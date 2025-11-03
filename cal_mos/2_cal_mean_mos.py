"""Compute per-system mean MOS per dimension and write summary files.

Outputs:
 - subjective_results/result_common.txt
 - subjective_results/result_pro.txt
The format is compatible with robustness score parser (Average Quality field).
"""

import os
import pandas as pd
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS
from utils.common import ensure_dir_exists

MOS_COLUMNS = ['复杂度','喜爱度','质量','一致性','实用性']


def calc_mean_mos(sys_id: str, dim: str, suffix: str):
    path = os.path.join(PATHS["preprocess_data_dir"], sys_id, dim)
    file_path = os.path.join(path, f'all_mos_{suffix}.csv')
    if not os.path.exists(file_path):
        return None, 0
    df = pd.read_csv(file_path)
    count = len(df)
    if count == 0:
        return {c: 0.0 for c in MOS_COLUMNS}, 0
    avg = df[MOS_COLUMNS].mean().to_dict()
    return avg, count


def calc_all_mean_mos():
    ensure_dir_exists(PATHS["subjective_result_dir"])
    out_common = os.path.join(PATHS["subjective_result_dir"], "result_common.txt")
    out_pro = os.path.join(PATHS["subjective_result_dir"], "result_pro.txt")
    # truncate
    open(out_common, 'w').close()
    open(out_pro, 'w').close()

    for sys_id in SYS_NAMES:
        for dim in EVAL_DIMS:
            for suffix, outfile in [("common", out_common), ("pro", out_pro)]:
                avg, count = calc_mean_mos(sys_id, dim, suffix)
                if avg is None:
                    continue
                print(f"====={sys_id}_{dim}_{suffix}=====")
                print(f"count: {count}")
                print(f"Average Complexity: {avg['复杂度']}")
                print(f"Average Enjoyment: {avg['喜爱度']}")
                print(f"Average Quality: {avg['质量']}")
                print(f"Average Alignment: {avg['一致性']}")
                print(f"Average Usefulness: {avg['实用性']}")
                with open(outfile, 'a', encoding='utf-8') as f:
                    f.write(f"====={sys_id}_{dim}=====\n")
                    f.write(f"count: {count}\n")
                    f.write(f"Average Complexity: {avg['复杂度']}\n")
                    f.write(f"Average Enjoyment: {avg['喜爱度']}\n")
                    f.write(f"Average Quality: {avg['质量']}\n")
                    f.write(f"Average Alignment: {avg['一致性']}\n")
                    f.write(f"Average Usefulness: {avg['实用性']}\n\n")


if __name__ == "__main__":
    calc_all_mean_mos()
