"""
Calculate clap scores for all wav samples
"""
import os
import json
import torch
from msclap import CLAP
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS, PROMPT_RANGES
from utils.common import load_prompts, ensure_dir

# 设置 CUDA 设备
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 加载各维度的提示词
acc_prompts = load_prompts(PATHS["acc_prompt_path"])
general_prompts = load_prompts(PATHS["general_prompt_path"])
robustness_prompts = load_prompts(PATHS["robustness_prompt_path"])
fairness_prompts = load_prompts(PATHS["fairness_prompt_path"])

def get_prompt_text(prompt_id: str) -> str:
    """根据 prompt ID 获取对应文本"""
    pid = int(prompt_id)
    if PROMPT_RANGES["acc"][0] <= pid <= PROMPT_RANGES["acc"][1]:
        return acc_prompts[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["generalization"][0] <= pid <= PROMPT_RANGES["generalization"][1]:
        return general_prompts[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["robustness"][0] <= pid <= PROMPT_RANGES["robustness"][1]:
        return robustness_prompts[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["fairness"][0] <= pid <= PROMPT_RANGES["fairness"][1]:
        return fairness_prompts[f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")

def cal_clap_score_for_jsonl(input_jsonl: str, result_jsonl: str):
    """计算 JSONL 文件中所有音频的 CLAP 分数"""
    ensure_dir(os.path.dirname(result_jsonl))
    clap_model = CLAP(version='2023', use_cuda=True)

    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            file_path = data['path']
            prompt_id = file_path.split('/')[-1].split('_')[1].replace('.wav','').replace('P','')
            prompt_text = get_prompt_text(prompt_id)

            audio_emb = clap_model.get_audio_embeddings([file_path])
            text_emb = clap_model.get_text_embeddings([prompt_text])
            score = torch.nn.functional.cosine_similarity(audio_emb, text_emb).item()

            print(f"{file_path} similarity_score: {score}")
            with open(result_jsonl, 'a', encoding='utf-8') as out_f:
                json.dump({"CLAP": score}, out_f)
                out_f.write('\n')

def calculate_all_clap_scores():
    """循环计算所有系统、维度的 CLAP 分数"""
    ensure_dir(PATHS["clap_results_dir"])
    for sys_name in SYS_NAMES:
        for eval_dim in EVAL_DIMS:
            temp = f"{sys_name}_{eval_dim}"
            input_jsonl = os.path.join(PATHS["prepared_jsonl_dir"], f"{temp}.jsonl")
            result_jsonl = os.path.join(PATHS["clap_results_dir"], f"{temp}.jsonl")
            print(f"====={temp}=====")
            cal_clap_score_for_jsonl(input_jsonl, result_jsonl)

if __name__ == "__main__":
    calculate_all_clap_scores()
