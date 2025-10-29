"""
步骤1：
遍历每个系统（System）和评估维度（Dimension），
查找对应目录下的所有 WAV 文件，
并生成 JSONL 格式的输入文件供后续模块使用。

示例输出文件：
  /home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/audiogen_acc.jsonl
"""

import os
from utils.common import find_wav_files, save_to_jsonl, ensure_dir
from utils.config import SYS_NAMES, EVAL_DIMS, SAMPLE_PATH, PREPARED_JSONL_DIR


def prepare_aes_inputs():
    """主函数：批量生成输入 JSONL 文件"""

    ensure_dir(PREPARED_JSONL_DIR)

    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            # 构造当前系统维度下的样本路径
            # e.g. 
            input_dir = os.path.join(SAMPLE_PATH, sys_name, eval_dim)

            if not os.path.exists(input_dir):
                print(f"警告: 目录不存在，跳过 {input_dir}")
                continue

            # 递归获取所有 .wav 文件路径
            wav_files = find_wav_files(input_dir)
            if not wav_files:
                print(f"警告: {input_dir} 下未找到任何 WAV 文件。")
                continue

            # 输出文件名，如 audiogen_acc.jsonl
            output_jsonl = os.path.join(
                PREPARED_JSONL_DIR, f"{sys_name}_{eval_dim}.jsonl"
            )

            save_to_jsonl(wav_files, output_jsonl)
            print(f"已生成输入文件: {output_jsonl}，共 {len(wav_files)} 条。")


if __name__ == "__main__":
    prepare_aes_inputs()
    print("✅ AES 输入文件准备完成！")
