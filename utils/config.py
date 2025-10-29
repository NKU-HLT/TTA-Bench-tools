import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 系统名称列表
SYS_NAMES = [
    "audiogen",
    "magnet", "stable_audio", "make_an_audio", "make_an_audio_2",
    "audioldm-l-full", "audioldm2-large", "auffusion-full", "tango-full", "tango2-full"
]

# 评估维度
EVAL_DIMS = [
    "acc",
    "generalization",
    "robustness",
    "fairness"
]

# 文件路径配置
PATHS = {
    "clap_results_dir": os.path.join(PROJECT_ROOT, "clap_results"),
    "acc_prompt_path": os.path.join(PROJECT_ROOT, "prompt/acc_prompt.json"),
    "general_prompt_path": os.path.join(PROJECT_ROOT, "prompt/generalization_prompt.json"),
    "robustness_prompt_path": os.path.join(PROJECT_ROOT, "prompt/robustness_prompt.json"),
    "fairness_prompt_path": os.path.join(PROJECT_ROOT, "prompt/fairness_prompt.json"),
}

# AES输入、输出jsonl存放路径
PREPARED_JSONL_DIR =  os.path.join(PROJECT_ROOT, "prepared_jsonl")
AES_RESULTS_JSON_DIR = os.path.join(PROJECT_ROOT, "aes_results")
AES_RESULT_FILE = os.path.join(AES_RESULTS_JSON_DIR, "result.txt")
AES_ATTR_FILE = os.path.join(AES_RESULTS_JSON_DIR, "attr_result.txt")
# 存放全部音频样本路径
SAMPLE_PATH = "/home/liucheng/project/tta-benchmark/samples/"

# prompt id 范围
PROMPT_RANGES = {
    "acc": [1, 1500],
    "generalization": [1501, 1800],
    "robustness": [1801, 2100],
    "fairness": [2101, 2400],
}
