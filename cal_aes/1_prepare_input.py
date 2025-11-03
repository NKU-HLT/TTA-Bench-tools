"""
Step 1: Prepare inputs for AES scoring.
- Iterate all systems and dimensions
- Collect all .wav files under samples
- Write JSONL files for downstream batch scoring

Example output:
    prepared_jsonl/audiogen_acc.jsonl
"""

import os
from utils.common import find_wav_files, save_to_jsonl, ensure_dir
from utils.config import SYS_NAMES, EVAL_DIMS, SAMPLE_PATH, PATHS


def prepare_aes_inputs():
    """主函数：批量生成输入 JSONL 文件"""

    prepared_dir = PATHS["prepared_jsonl_dir"]
    ensure_dir(prepared_dir)

    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            # Construct sample directory for current system/dimension
            input_dir = os.path.join(SAMPLE_PATH, sys_name, eval_dim)

            if not os.path.exists(input_dir):
                print(f"[Warn] Directory not found, skip: {input_dir}")
                continue

            # 递归获取所有 .wav 文件路径
            wav_files = find_wav_files(input_dir)
            if not wav_files:
                print(f"[Warn] No WAV files found under: {input_dir}")
                continue

            # 输出文件名，如 audiogen_acc.jsonl
            output_jsonl = os.path.join(prepared_dir, f"{sys_name}_{eval_dim}.jsonl")

            save_to_jsonl(wav_files, output_jsonl)
            print(f"Prepared: {output_jsonl} with {len(wav_files)} entries.")


if __name__ == "__main__":
    prepare_aes_inputs()
    print("AES input preparation done.")
