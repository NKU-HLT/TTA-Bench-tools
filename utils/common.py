# common.py

import os
import csv
import json
import pandas as pd

def ensure_dir(directory):
    """确保目录存在，不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def find_wav_files(directory):
    """递归查找指定目录下的所有 WAV 文件"""
    wav_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    return wav_files

def save_to_jsonl(file_list, output_file):
    """将文件路径列表写入 JSONL 文件"""
    ensure_dir(os.path.dirname(output_file))
    with open(output_file, "w", encoding="utf-8") as f:
        for file_path in file_list:
            json_line = json.dumps({"path": file_path}, ensure_ascii=False)
            f.write(json_line + "\n")

def load_prompts(prompt_path: str, target_field: str) -> dict:
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return {prompt_data['id']: prompt_data[target_field] for prompt_data in prompts}

def process_csv(input_csv_path, output_csv_path, person_id, prompt_id, dim):
    """处理CSV数据，按需分配到对应的输出文件"""
    # 读取CSV文件
    df = pd.read_csv(input_csv_path)

    # 如果输出文件不存在，则创建并写入表头
    if not os.path.exists(output_csv_path):
        ensure_dir(os.path.dirname(output_csv_path))
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['wav_name', 'person_id', '复杂度', '喜爱度', '质量', '一致性', '实用性'])

    # 文件已存在，将当前行数据写入对应的输出文件
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for index, row in df.iterrows():
            wav_name = row['name']  # S001_P0001.wav
            writer.writerow([wav_name, person_id, row['复杂度'], row['喜爱度'], row['质量'], row['一致性'], row['实用性']])

def get_dimension(prompt_id, prompt_ranges):
    """根据prompt ID获取对应的维度"""
    for dim, (start, end) in prompt_ranges.items():
        if start <= prompt_id <= end:
            return dim
    raise ValueError(f"Invalid prompt ID: {prompt_id}")

def get_prompt_attr(prompt_id, prompt_files):
    """根据prompt ID获取属性"""
    if 1 <= int(prompt_id) <= 1500:
        acc_data = load_json(prompt_files["acc"])
        event_count = acc_data.get(f"prompt_{prompt_id}", {}).get("event_count", "unknown")
        event_relation = acc_data.get(f"prompt_{prompt_id}", {}).get("event_relation", "unknown")
        return event_count, event_relation
    elif 1501 <= int(prompt_id) <= 1800:
        general_data = load_json(prompt_files["generalization"])
        return general_data.get(f"prompt_{prompt_id}", {}).get("event_count", "unknown")
    elif 1801 <= int(prompt_id) <= 2100:
        robustness_data = load_json(prompt_files["robustness"])
        return robustness_data.get(f"prompt_{prompt_id}", {}).get("perturbation_type", "unknown")
    elif 2101 <= int(prompt_id) <= 2400:
        fairness_data = load_json(prompt_files["fairness"])
        return fairness_data.get(f"prompt_{prompt_id}", {}).get("notes", "unknown")
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")

