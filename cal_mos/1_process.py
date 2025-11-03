"""Preprocess raw MOS csv annotations into per-system files per dimension.

Expected input CSV columns include Chinese headers from annotation tool:
 - name, 复杂度, 喜爱度, 质量, 一致性, 实用性
"""

import os
import pandas as pd
from utils.config import PATHS, PROMPT_RANGES
from utils.common import ensure_dir_exists, get_dimension, write_mos_csv

def process_csv(input_csv_path: str, suffix: str):
    df = pd.read_csv(input_csv_path)
    person_id = os.path.basename(input_csv_path).split('-')[1].split('.')[0]

    for _, row in df.iterrows():
        wav_name = row['name']
        system_id = wav_name.split('_')[0]
        if system_id == "S000":  # probe item, skip
            continue
        prompt_id = int(wav_name.split('_')[1].replace('P',''))
        dim = get_dimension(prompt_id, PROMPT_RANGES)
        output_csv_path = os.path.join(PATHS["preprocess_data_dir"], system_id, dim, f'all_mos_{suffix}.csv')
        write_mos_csv(output_csv_path, [
            wav_name, person_id, row['复杂度'], row['喜爱度'],
            row['质量'], row['一致性'], row['实用性']
        ])
    print(f"Processed: {input_csv_path}")

def process_all_mos():
    ensure_dir_exists(PATHS["preprocess_data_dir"])
    for input_csv_path in os.listdir(PATHS["mos_common_input_dir"]):
        process_csv(os.path.join(PATHS["mos_common_input_dir"], input_csv_path), 'common')
    for input_csv_path in os.listdir(PATHS["mos_pro_input_dir"]):
        process_csv(os.path.join(PATHS["mos_pro_input_dir"], input_csv_path), 'pro')

if __name__ == "__main__":
    process_all_mos()
