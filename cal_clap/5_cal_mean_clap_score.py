"""
Calculate mean clap scores for each dimension of each system
"""
import os
import json
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS
from utils.common import ensure_dir

def calculate_mean_clap_scores():
    """计算每个系统每个维度的平均 CLAP 分数"""
    ensure_dir(PATHS["clap_results_dir"])
    outfile = os.path.join(PATHS["clap_results_dir"], "result.txt")

    with open(outfile, 'w') as f:
        for sys_name in SYS_NAMES:
            for eval_dim in EVAL_DIMS:
                temp = f"{sys_name}_{eval_dim}"
                result_jsonl = os.path.join(PATHS["clap_results_dir"], f"{temp}.jsonl")
                total, count = 0, 0
                with open(result_jsonl, 'r') as r_f:
                    for line in r_f:
                        total += json.loads(line)["CLAP"]
                        count += 1
                avg = total / count if count > 0 else 0
                print(f"====={temp}=====")
                print(f"count: {count} Average CLAP: {avg}")
                f.write(f"{temp}\n{avg}\n")

if __name__ == "__main__":
    calculate_mean_clap_scores()
