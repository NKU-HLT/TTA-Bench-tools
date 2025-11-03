"""
Calculate mean aes scores for each attribute of each dimension of each system
"""

import os
import json
from utils.common import get_prompt_attr
from utils.config import SYS_NAMES, EVAL_DIMS, AES_RESULTS_JSON_DIR, PATHS, AES_ATTR_FILE


def summarize_aes_scores():
    """Aggregate attribute-level AES metrics for each system x dimension."""

    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            temp = f"{sys_name}_{eval_dim}.jsonl"
            # e.g. audiogen_acc.jsonl, audioldm_robustness.jsonl
            input_jsonl = os.path.join(PATHS["prepared_jsonl_dir"], temp)
            score_jsonl = os.path.join(AES_RESULTS_JSON_DIR, temp)

            # key:prompt_attr,value:{key:total_ce/cu/pc/pq/count,value}
            results = {}

            with open(input_jsonl, 'r') as input_file, open(score_jsonl, 'r') as score_file:
                for input_line, score_line in zip(input_file, score_file):
                    input_data = json.loads(input_line)  # {"path": "/path/to/.../S001_P0422.wav"}
                    score_data = json.loads(score_line)  # {"CE": ..., "CU": ..., "PC": ..., "PQ": ...}

                    file_path = input_data['path']
                    prompt_id = file_path.split('/')[-1].split('_')[1].replace('.wav', '').replace("P","")  # "0001"
                    prompt_attr = get_prompt_attr(prompt_id)

                    if prompt_attr not in results:
                        results[prompt_attr] = {
                            'total_ce': 0,
                            'total_cu': 0,
                            'total_pc': 0,
                            'total_pq': 0,
                            'count': 0
                        }

                    results[prompt_attr]['total_ce'] += score_data['CE']
                    results[prompt_attr]['total_cu'] += score_data['CU']
                    results[prompt_attr]['total_pc'] += score_data['PC']
                    results[prompt_attr]['total_pq'] += score_data['PQ']
                    results[prompt_attr]['count'] += 1

            # Append to a single attribute result file used by fairness calculator
            with open(AES_ATTR_FILE, 'a', encoding='utf-8') as output_file:
                for attr, data in results.items():
                    count = data['count']
                    if count > 0:
                        avg_ce = data['total_ce'] / count
                        avg_cu = data['total_cu'] / count
                        avg_pc = data['total_pc'] / count
                        avg_pq = data['total_pq'] / count
                    else:
                        avg_ce = avg_cu = avg_pc = avg_pq = 0

                    tag = f"{sys_name}_{eval_dim}"
                    print(f"====={tag}_{attr}=====")
                    print(f"count: {count}")
                    print(f"Average CE: {avg_ce}")
                    print(f"Average CU: {avg_cu}")
                    print(f"Average PC: {avg_pc}")
                    print(f"Average PQ: {avg_pq}")
                    
                    output_file.write(f"====={tag}_{attr}=====\n")
                    output_file.write(f"count: {count}\n")
                    output_file.write(f"Average CE: {avg_ce}\n")
                    output_file.write(f"Average CU: {avg_cu}\n")
                    output_file.write(f"Average PC: {avg_pc}\n")
                    output_file.write(f"Average PQ: {avg_pq}\n")
                    output_file.write("\n")


if __name__ == "__main__":
    summarize_aes_scores()
