"""
Calculate aes scores for all wav samples
"""
import os
from utils.config import SYS_NAMES, EVAL_DIMS, PREPARED_JSONL_DIR, AES_RESULTS_JSON_DIR
from utils.common import ensure_dir

# 指定 GPU 设备
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
BATCH_SIZE = 32

def calculate_all_aes_scores():
    """遍历所有系统与维度，执行 AES 计算"""
    ensure_dir(AES_RESULTS_JSON_DIR)

    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            tag = f"{sys_name}_{eval_dim}"
            input_jsonl = os.path.join(PREPARED_JSONL_DIR, f"{tag}.jsonl")
            result_jsonl = os.path.join(AES_RESULTS_JSON_DIR, f"{tag}.jsonl")

            command = f"audio-aes {input_jsonl} --batch-size {BATCH_SIZE} > {result_jsonl}"
            print(f"开始计算 {tag} 的 AES 分数...")
            os.system(command)
            print(f"AES 结果已保存至 {result_jsonl}")

if __name__ == "__main__":
    calculate_all_aes_scores()
