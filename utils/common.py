import os
import csv
import json
import pandas as pd
from typing import Dict, Any, Tuple

from utils.config import PATHS, PROMPT_RANGES


def ensure_dir(directory: str):
    """Create directory if it does not exist."""
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def ensure_dir_exists(directory: str):
    """Alias of ensure_dir for backward compatibility."""
    ensure_dir(directory)


def find_wav_files(directory: str):
    """Recursively find all .wav files under a directory."""
    wav_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    return wav_files


def save_to_jsonl(file_list, output_file):
    """Write a list of file paths into a JSONL file under the key 'path'."""
    ensure_dir(os.path.dirname(output_file))
    with open(output_file, "w", encoding="utf-8") as f:
        for file_path in file_list:
            json_line = json.dumps({"path": file_path}, ensure_ascii=False)
            f.write(json_line + "\n")


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_prompts(prompt_path: str, target_field: str) -> dict:
    """Load prompt json and return a mapping from id to a specific field."""
    prompts = load_json(prompt_path)
    return {p["id"]: p[target_field] for p in prompts}


def write_mos_csv(output_csv_path: str, row_values):
    """Append a row to MOS CSV; create file with header if needed.

    Header columns (Chinese kept to match raw annotation files):
    ['wav_name', 'person_id', '复杂度', '喜爱度', '质量', '一致性', '实用性']
    """
    header = ['wav_name', 'person_id', '复杂度', '喜爱度', '质量', '一致性', '实用性']
    if not os.path.exists(output_csv_path):
        ensure_dir(os.path.dirname(output_csv_path))
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row_values)


def get_dimension(prompt_id: int, prompt_ranges: Dict[str, Tuple[int, int]]):
    """Return dimension name for a given prompt id using configured ranges."""
    for dim, (start, end) in prompt_ranges.items():
        if start <= prompt_id <= end:
            return dim
    raise ValueError(f"Invalid prompt ID: {prompt_id}")


def get_prompt_text(prompt_id: str) -> str:
    """Return the textual prompt for a given prompt id.

    Tries the 'text' field first; if unavailable, tries common variants.
    """
    pid = int(prompt_id)
    # Determine which prompt file to use by range
    if PROMPT_RANGES["acc"][0] <= pid <= PROMPT_RANGES["acc"][1]:
        prompt_path = PATHS["acc_prompt_path"]
    elif PROMPT_RANGES["generalization"][0] <= pid <= PROMPT_RANGES["generalization"][1]:
        prompt_path = PATHS["general_prompt_path"]
    elif PROMPT_RANGES["robustness"][0] <= pid <= PROMPT_RANGES["robustness"][1]:
        prompt_path = PATHS["robustness_prompt_path"]
    elif PROMPT_RANGES["fairness"][0] <= pid <= PROMPT_RANGES["fairness"][1]:
        prompt_path = PATHS["fairness_prompt_path"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")

    prompts = load_json(prompt_path)
    key = f"prompt_{prompt_id}"
    # Build an id->object map if needed
    index = {p["id"]: p for p in prompts}
    obj = index.get(key)
    if obj is None:
        raise KeyError(f"Prompt id {key} not found in {prompt_path}")
    for field in ("text", "prompt", "description"):
        if field in obj:
            return obj[field]
    raise KeyError(f"No text-like field found for {key} in {prompt_path}")


def get_prompt_attr(prompt_id: str):
    """Return attribute label(s) for a prompt id depending on dimension.

    - acc: returns (event_count, event_relation)
    - generalization: returns event_count
    - robustness: returns perturbation_type
    - fairness: returns notes
    """
    pid = int(prompt_id)
    if PROMPT_RANGES["acc"][0] <= pid <= PROMPT_RANGES["acc"][1]:
        acc_event_count = load_prompts(PATHS["acc_prompt_path"], "event_count")
        acc_event_relation = load_prompts(PATHS["acc_prompt_path"], "event_relation")
        return acc_event_count[f"prompt_{prompt_id}"], acc_event_relation[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["generalization"][0] <= pid <= PROMPT_RANGES["generalization"][1]:
        general_event_count = load_prompts(PATHS["general_prompt_path"], "event_count")
        return general_event_count[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["robustness"][0] <= pid <= PROMPT_RANGES["robustness"][1]:
        robust_type = load_prompts(PATHS["robustness_prompt_path"], "perturbation_type")
        return robust_type[f"prompt_{prompt_id}"]
    elif PROMPT_RANGES["fairness"][0] <= pid <= PROMPT_RANGES["fairness"][1]:
        fairness_notes = load_prompts(PATHS["fairness_prompt_path"], "notes")
        return fairness_notes[f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")

