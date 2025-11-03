import os

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# System identifiers (folder names under samples/)
SYS_NAMES = [
    "audiogen",
    "magnet", "stable_audio", "make_an_audio", "make_an_audio_2",
    "audioldm-l-full", "audioldm2-large", "auffusion-full", "tango-full", "tango2-full"
]

# Evaluation dimensions (dataset splits)
EVAL_DIMS = [
    "acc",
    "generalization",
    "robustness",
    "fairness"
]

# Prompt id ranges for each dimension
PROMPT_RANGES = {
    "acc": [1, 1500],
    "generalization": [1501, 1800],
    "robustness": [1801, 2100],
    "fairness": [2101, 2400],
}

# File and directory layout
PATHS = {
    # Data roots
    "samples_root": "/home/liucheng/project/tta-benchmark/samples/",

    # Prompt jsons
    "acc_prompt_path": os.path.join(PROJECT_ROOT, "prompts/acc_prompt.json"),
    "general_prompt_path": os.path.join(PROJECT_ROOT, "prompts/generalization_prompt.json"),
    "robustness_prompt_path": os.path.join(PROJECT_ROOT, "prompts/robustness_prompt.json"),
    "fairness_prompt_path": os.path.join(PROJECT_ROOT, "prompts/fairness_prompt.json"),
    "prompts_dir": os.path.join(PROJECT_ROOT, "prompts"),

    # Prepared jsonl for batch scoring
    "prepared_jsonl_dir": os.path.join(PROJECT_ROOT, "prepared_jsonl"),

    # AES outputs
    "aes_results_dir": os.path.join(PROJECT_ROOT, "aes_results"),
    # CLAP outputs
    "clap_results_dir": os.path.join(PROJECT_ROOT, "clap_results"),

    # MOS processing
    "preprocess_data_dir": os.path.join(PROJECT_ROOT, "preprocess_data"),
    "mos_common_input_dir": os.path.join(PROJECT_ROOT, "mos_input", "common"),
    "mos_pro_input_dir": os.path.join(PROJECT_ROOT, "mos_input", "pro"),
    "subjective_result_dir": os.path.join(PROJECT_ROOT, "subjective_results"),
}

# AES outputs
AES_RESULTS_JSON_DIR = PATHS["aes_results_dir"]
AES_RESULT_FILE = os.path.join(AES_RESULTS_JSON_DIR, "result.txt")
# Attribute-level AES aggregation file (used by fairness scoring)
AES_ATTR_FILE = os.path.join(AES_RESULTS_JSON_DIR, "aes_attribute_results.txt")

# Where to read audio samples from
SAMPLE_PATH = PATHS["samples_root"]
