"""
Calculate clap scores for all wav samples
"""
import os
import json
import torch
from msclap import CLAP
from utils.config import SYS_NAMES, EVAL_DIMS, PATHS
from utils.common import ensure_dir, get_prompt_text

# Select CUDA device (optional)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# get_prompt_text is provided by utils.common

def cal_clap_score_for_jsonl(input_jsonl: str, result_jsonl: str):
    """Compute CLAP scores for all entries in a JSONL file."""
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
    """Loop over all systems x dimensions and compute CLAP scores."""
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
