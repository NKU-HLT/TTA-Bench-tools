"""
Calculate mean clap scores for each attribute of each dimension of each system
"""
import os
import json
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS, PROMPT_RANGES
from utils.common import ensure_dir, load_prompts

# 加载各维度提示词及属性字段
acc_event_count_map = load_prompts(PATHS["acc_prompt_path"], "event_count")
acc_event_relation_map = load_prompts(PATHS["acc_prompt_path"], "event_relation")
general_event_count_map = load_prompts(PATHS["general_prompt_path"], "event_count")
robustness_type_map = load_prompts(PATHS["robustness_prompt_path"], "perturbation_type")
fairness_type_map = load_prompts(PATHS["fairness_prompt_path"], "notes")

def get_prompt_attr(prompt_id: str):
    """根据 prompt ID 获取属性"""
    pid = int(prompt_id)
    if PROMPT_RANGES["acc"][0] <= pid <= PROMPT_RANGES["acc"][1]:
        return acc_event_count_map[f"prompt_{prompt_id}"], acc_event_relation_map[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["generalization"][0] <= pid <= PROMPT_RANGES["generalization"][1]:
        return general_event_count_map[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["robustness"][0] <= pid <= PROMPT_RANGES["robustness"][1]:
        return robustness_type_map[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["fairness"][0] <= pid <= PROMPT_RANGES["fairness"][1]:
        return fairness_type_map[f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")

def calculate_attr_clap_scores():
    """计算每个系统每个维度每个属性的平均 CLAP 分数"""
    ensure_dir(PATHS["clap_results_dir"])
    output_txt = os.path.join(PATHS["clap_results_dir"], "clap_attribute_results.txt")
    # 清空文件
    with open(output_txt, 'w') as f: pass

    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            temp = f"{sys_name}_{eval_dim}"
            input_jsonl = os.path.join(PATHS["prepared_jsonl_dir"], f"{temp}.jsonl")
            score_jsonl = os.path.join(PATHS["clap_results_dir"], f"{temp}.jsonl")
            results = {}

            with open(input_jsonl, 'r') as in_f, open(score_jsonl, 'r') as score_f:
                for in_line, score_line in zip(in_f, score_f):
                    file_path = json.loads(in_line)["path"]
                    score_val = json.loads(score_line)["CLAP"]
                    prompt_id = file_path.split('/')[-1].split('_')[1].replace('.wav','').replace('P','')
                    prompt_attr = get_prompt_attr(prompt_id)
                    if prompt_attr not in results:
                        results[prompt_attr] = {'total_clap': 0, 'count': 0}
                    results[prompt_attr]['total_clap'] += score_val
                    results[prompt_attr]['count'] += 1

            with open(output_txt, 'a') as out_f:
                for attr, data in results.items():
                    avg = data['total_clap']/data['count'] if data['count']>0 else 0
                    print(f"====={temp}_{attr}=====")
                    print(f"count:{data['count']} Average CLAP:{avg}")
                    out_f.write(f"====={temp}_{attr}=====\n")
                    out_f.write(f"count:{data['count']}\nAverage CLAP:{avg}\n\n")

if __name__ == "__main__":
    calculate_attr_clap_scores()
