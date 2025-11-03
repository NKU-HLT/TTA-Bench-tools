"""Compute attribute-level MOS for each system x dimension.

Outputs:
 - subjective_results/attr_result_common.txt
 - subjective_results/attr_result_pro.txt
Header fields are in English (Average Complexity/Quality/etc.) for downstream parsers.
"""

import os
import pandas as pd
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS
from utils.common import ensure_dir_exists, get_prompt_attr


MOS_COLUMNS = ['复杂度','喜爱度','质量','一致性','实用性']


def calc_attr_mos(sys_ids, eval_dims, suffixes=("common", "pro")):
    ensure_dir_exists(PATHS["subjective_result_dir"])

    for sys_id in sys_ids:
        for dim in eval_dims:
            search_path = os.path.join(PATHS["preprocess_data_dir"], sys_id, dim)

            for suffix in suffixes:
                file_path = os.path.join(search_path, f'all_mos_{suffix}.csv')
                if not os.path.exists(file_path):
                    print(f"[Warn] Missing file: {file_path}")
                    continue

                df = pd.read_csv(file_path)
                results = {}

                for _, row in df.iterrows():
                    wav_name = row['wav_name']
                    prompt_id = wav_name.split('_')[1].replace('.wav','').replace('P','')
                    prompt_attr = get_prompt_attr(prompt_id)

                    key = prompt_attr if isinstance(prompt_attr, str) else tuple(prompt_attr)

                    if key not in results:
                        results[key] = {col: 0 for col in MOS_COLUMNS}
                        results[key]['count'] = 0

                    for col in MOS_COLUMNS:
                        results[key][col] += row[col]
                    results[key]['count'] += 1

                # Write averages
                outfile = os.path.join(PATHS["subjective_result_dir"], f'attr_result_{suffix}.txt')
                with open(outfile, 'a', encoding='utf-8') as f:
                    for attr, data in results.items():
                        count = data['count']
                        avg = {col: (data[col] / count if count > 0 else 0) for col in MOS_COLUMNS}
                        print(f"====={sys_id}_{dim}_{attr}_{suffix}=====")
                        print(f"count: {count}")
                        print(f"Average Complexity: {avg['复杂度']}")
                        print(f"Average Enjoyment: {avg['喜爱度']}")
                        print(f"Average Quality: {avg['质量']}")
                        print(f"Average Alignment: {avg['一致性']}")
                        print(f"Average Usefulness: {avg['实用性']}")
                        f.write(f"====={sys_id}_{dim}_{attr}=====\n")
                        f.write(f"count: {count}\n")
                        f.write(f"Average Complexity: {avg['复杂度']}\n")
                        f.write(f"Average Enjoyment: {avg['喜爱度']}\n")
                        f.write(f"Average Quality: {avg['质量']}\n")
                        f.write(f"Average Alignment: {avg['一致性']}\n")
                        f.write(f"Average Usefulness: {avg['实用性']}\n\n")


if __name__ == "__main__":
    calc_attr_mos(SYS_NAMES, EVAL_DIMS)
