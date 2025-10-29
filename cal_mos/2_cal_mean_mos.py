# cal_mos/cal_mean_mos.py

import os
import pandas as pd
from utils.config import SYS_IDS, EVAL_DIMS, PATHS
from utils.common import ensure_dir_exists

MOS_COLUMNS = ['复杂度','喜爱度','质量','一致性','实用性']

def calc_mean_mos(sys_id, dim):
    path = os.path.join(PATHS["preprocess_data_dir"], sys_id, dim)
    result = {}
    for suffix in ['common','pro']:
        file_path = os.path.join(path, f'all_mos_{suffix}.csv')
        df = pd.read_csv(file_path)
        avg = df[MOS_COLUMNS].mean().to_dict()
        result[suffix] = avg
    return result

def calc_all_mean_mos():
    ensure_dir_exists(PATHS["subjective_result_dir"])
    for sys_id in SYS_IDS:
        for dim in EVAL_DIMS.keys():
            mean_result = calc_mean_mos(sys_id, dim)
            print(f"====={sys_id}_{dim}=====")
            print(mean_result)

if __name__ == "__main__":
    calc_all_mean_mos()
