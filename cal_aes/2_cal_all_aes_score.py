"""
Step 2: Calculate AES scores for all wav samples listed in prepared JSONL files.
"""
import os
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS, AES_RESULTS_JSON_DIR
from utils.common import ensure_dir

# Select GPU device (optional)
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
BATCH_SIZE = 32

def calculate_all_aes_scores():
    """Iterate all systems/dimensions and run AES CLI to produce JSONL scores."""
    ensure_dir(AES_RESULTS_JSON_DIR)
    prepared_dir = PATHS["prepared_jsonl_dir"]

    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            tag = f"{sys_name}_{eval_dim}"
            input_jsonl = os.path.join(prepared_dir, f"{tag}.jsonl")
            result_jsonl = os.path.join(AES_RESULTS_JSON_DIR, f"{tag}.jsonl")

            command = f"audio-aes {input_jsonl} --batch-size {BATCH_SIZE} > {result_jsonl}"
            print(f"Compute AES for {tag}...")
            os.system(command)
            print(f"AES results saved to {result_jsonl}")

if __name__ == "__main__":
    calculate_all_aes_scores()
