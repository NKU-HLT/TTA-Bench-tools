# cal_mos/cal_attr_mos.py

import os
import pandas as pd
from utils.config import SYS_IDS, EVAL_DIMS, PATHS, PROMPT_FIELDS
from utils.common import ensure_dir_exists, load_prompts, get_dimension

# ===============================
# 1. 加载prompt属性映射
# ===============================

def load_all_prompt_maps():
    prompt_maps = {}
    prompts_dir = PATHS["prompts_dir"]
    for dim, fields in PROMPT_FIELDS.items():
        dim_maps = {}
        for field in fields:
            prompt_file = os.path.join(prompts_dir, f"{dim}_prompt.json")
            dim_maps[field] = load_prompts(prompt_file, field)
        prompt_maps[dim] = dim_maps
    return prompt_maps

PROMPT_MAPS = load_all_prompt_maps()


# ===============================
# 2. 根据prompt_id获取对应属性
# ===============================
def get_prompt_attr(dim: str, prompt_id: str):
    """根据维度和prompt_id返回对应的属性"""
    if dim not in PROMPT_MAPS:
        raise ValueError(f"Invalid dimension: {dim}")
    dim_map = PROMPT_MAPS[dim]
    if dim == "acc":
        return (
            dim_map["event_count"][f"prompt_{prompt_id}"],
            dim_map["event_relation"][f"prompt_{prompt_id}"]
        )
    elif dim in ["generalization", "robustness", "fairness"]:
        field = list(dim_map.keys())[0]  # 每个维度只有一个属性字段
        return dim_map[field][f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt_id: {prompt_id}")


# ===============================
# 3. 计算属性MOS
# ===============================
MOS_COLUMNS = ['复杂度','喜爱度','质量','一致性','实用性']

def calc_attr_mos(sys_ids, eval_dims, suffixes=['common','pro']):
    ensure_dir_exists(PATHS["subjective_result_dir"])

    for sys_id in sys_ids:
        for dim in eval_dims:
            search_path = os.path.join(PATHS["preprocess_data_dir"], sys_id, dim)

            for suffix in suffixes:
                file_path = os.path.join(search_path, f'all_mos_{suffix}.csv')
                if not os.path.exists(file_path):
                    print(f"文件不存在: {file_path}")
                    continue

                df = pd.read_csv(file_path)
                results = {}

                for _, row in df.iterrows():
                    wav_name = row['wav_name']
                    prompt_id = wav_name.split('_')[1].replace('.wav','').replace('P','')
                    prompt_attr = get_prompt_attr(dim, prompt_id)

                    # 对于acc返回的是tuple，其余是str
                    key = prompt_attr if isinstance(prompt_attr, str) else tuple(prompt_attr)

                    if key not in results:
                        results[key] = {col:0 for col in MOS_COLUMNS}
                        results[key]['count'] = 0

                    for col in MOS_COLUMNS:
                        results[key][col] += row[col]
                    results[key]['count'] += 1

                # 输出平均MOS
                outfile = os.path.join(PATHS["subjective_result_dir"], f'attr_result_{suffix}.txt')
                with open(outfile, 'a', encoding='utf-8') as f:
                    for attr, data in results.items():
                        count = data['count']
                        avg = {col:data[col]/count if count>0 else 0 for col in MOS_COLUMNS}
                        print(f"====={sys_id}_{dim}_{attr}_{suffix}=====")
                        print(f"count:{count}")
                        for col in MOS_COLUMNS:
                            print(f"Average {col}: {avg[col]}")
                        f.write(f"====={sys_id}_{dim}_{attr}=====\n")
                        f.write(f"count: {count}\n")
                        for col in MOS_COLUMNS:
                            f.write(f"Average {col}: {avg[col]}\n")
                        f.write("\n")


if __name__ == "__main__":
    # 可以选择只处理部分系统或维度
    calc_attr_mos(SYS_IDS, EVAL_DIMS.keys())
