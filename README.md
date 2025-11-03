
# 📦 TTA-Bench-tools
> Utilities for computing metrics and aggregations for TTA-Bench: AES, CLAP, MOS, Fairness, and Robustness.
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Project Page](https://img.shields.io/badge/Project-Website-blue.svg)](https://jiusansan222.github.io/tta-bench/)
[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2509.02398-b31b1b.svg)](https://arxiv.org/abs/2509.02398)

## Overview
This repository provides end-to-end scripts to:
- Prepare inputs and compute AES ([Audiobox Aesthetics](https://github.com/facebookresearch/audiobox-aesthetics)) scores
- Compute CLAP similarities and aggregate system/attribute means
- Process human MOS annotations to system-level and attribute-level summaries
- Compute Fairness scores from MOS attribute-level results
- Compute Robustness scores as the ratio between perturbed and baseline quality

The tools are designed specifically for the [TTA-Bench](https://arxiv.org/abs/2509.02398) dataset structure and prompt files.

## Requirements
- Python 3.8+
- [microsoft/CLAP](https://github.com/microsoft/CLAP)
- [Audiobox-aesthetics](https://github.com/facebookresearch/audiobox-aesthetics)

## Usage
All pipelines are invoked by bash scripts from the repo root.
### AES
```bash
bash run_cal_aes.sh
```
This will run:
- cal_aes/1_prepare_input.py → prepared_jsonl/{system}_{dim}.jsonl

```bash
# example: prepared_jsonl/audiogen_acc.jsonl
{"path": "/home/liucheng/project/tta-benchmark/samples/audiogen/acc/S001_P0909.wav"}
{"path": "/home/liucheng/project/tta-benchmark/samples/audiogen/acc/S001_P0422.wav"}
{"path": "/home/liucheng/project/tta-benchmark/samples/audiogen/acc/S001_P0097.wav"}
...
```
- cal_aes/2_cal_all_aes_score.py → aes_results/{system}_{dim}.jsonl

```bash
# example: aes_results/audiogen_acc.jsonl
{"CE": 2.4572219848632812, "CU": 3.697906494140625, "PC": 3.3792734146118164, "PQ": 4.412182331085205}
{"CE": 2.626478672027588, "CU": 4.120411396026611, "PC": 3.2657086849212646, "PQ": 4.992600440979004}
{"CE": 3.7061448097229004, "CU": 4.163618564605713, "PC": 4.205262184143066, "PQ": 5.458792686462402}
...
```
- cal_aes/3_cal_mean_aes_score.py → aes_results/result.txt
```bash
# example: result.txt
audiogen_acc
2.88819442764918,4.541898544947307,3.1823971970876057,5.331650721232096
audiogen_generalization
2.9067096304893494,4.692270333766937,3.120330032110214,5.417774231433868
...
```
- cal_aes/6_cal_attr_aes_score.py → aes_results/aes_attribute_results.txt
```bash
# example: aes_attribute_result.txt
=====audiogen_acc_(5, 'complex')=====
count: 114
Average CE: 2.814668235025908
Average CU: 4.456804898747227
Average PC: 3.3684348265329995
Average PQ: 5.277690211931865

=====audiogen_acc_(1, 'None')=====
count: 280
Average CE: 2.8355861008167267
Average CU: 4.724663828951972
Average PC: 2.8160559394529887
Average PQ: 5.4647493575300485
...
```

### CLAP
```bash
bash run_cal_clap.sh
```
This will run:
- cal_clap/4_cal_all_clap_score.py → clap_results/{system}_{dim}.jsonl
```bash
# example: clap_results/audiogen_acc.jsonl; each line corresponds to a file path listed in prepared_jsonl/audiogen_acc.jsonl
{"CLAP": 0.27447181940078735}
{"CLAP": 0.5389132499694824}
{"CLAP": 0.7187406420707703}
...
```

- cal_clap/5_cal_mean_clap_score.py → clap_results/result.txt
```bash
# example: clap_results/result.txt
audiogen_acc
0.3940820222174128
audiogen_generalization
0.3374758129070203
audiogen_robustness
0.39479794369389615
...
```

- cal_clap/7_cal_attr_clap_score.py → clap_results/clap_attribute_results.txt
```bash
# example: clap_results/clap_attribute_results.txt
=====audiogen_acc_(5, 'complex')=====
count: 114
Average CLAP: 0.28634971751128896

=====audiogen_acc_(1, 'None')=====
count: 280
Average CLAP: 0.39908818397670986
...
```

### MOS (Mean Opinion Scores)

```bash
bash run_cal_mos.sh
```
This will run:
- cal_mos/1_process.py → process raw annotation CSVs from `mos_input/*` like following:
```bash
# Each CSV is expected to contain columns: `name, 复杂度, 喜爱度, 质量, 一致性, 实用性`.
preprocess_data/
├─ S001/                      
│  ├─ acc/                  
│  │  ├─ all_mos_common.csv
│  │  └─ all_mos_pro.csv
│  ├─ generalization/
│  │  ├─ all_mos_common.csv
│  │  └─ all_mos_pro.csv
│  ├─ robustness/
│  │  └─ all_mos_common.csv
│  └─ fairness/
│     └─ all_mos_common.csv
└─ S002/
    └─ ...
```
- cal_mos/2_cal_mean_mos.py → subjective_results/result_{common|pro}.txt
```bash
# example: subjective_results/result_common.txt
# MOS Dimensions: Average Complexity/Enjoyment/Quality/Alignment/Usefulness
S001_acc
3.542222222222222,3.1792592592592595,4.823703703703703,5.0814814814814815,3.637037037037037

S001_generalization
3.22962962962963,3.5481481481481483,5.437037037037037,5.948148148148148,4.518518518518518
...
```
- cal_mos/3_cal_attr_mos.py → subjective_results/attr_result_{common|pro}.txt
```bash
=====S001_acc_(2, 'sequence')=====
count: 87
Average Complexity: 3.1954022988505746
Average Enjoyment: 3.057471264367816
Average Quality: 5.149425287356322
Average Alignment: 5.057471264367816
Average Usefulness: 3.781609195402299

=====S001_acc_(2, 'parallelism')=====
count: 120
Average Complexity: 3.2
Average Enjoyment: 3.316666666666667
Average Quality: 4.983333333333333
Average Alignment: 6.05
Average Usefulness: 4.058333333333334
...
```

### Fairness
Compute Fairness scores from MOS attribute-level results:
```bash
bash run_fairness_score.sh
```
This calls:
- MOS fairness: `cal_fairness_score.py --input subjective_results/attr_result_common.txt --output subjective_results/fs_result_mos.txt`

The output file `subjective_results/fs_result_mos.txt` will contain per-system fairness for gender/age/language.


### Robustness
Requires MOS aggregation outputs:
- Baseline: `subjective_results/result_common.txt` (robustness dimension)
- Perturbed attributes: `subjective_results/attr_result_common.txt` (robustness attributes)
```bash
bash run_robustness_score.sh
```
This prints `robust_{attribute}` ratios and the overall mean per system.


## Citation

```
@misc{wang2025ttabenchcomprehensivebenchmarkevaluating,
      title={TTA-Bench: A Comprehensive Benchmark for Evaluating Text-to-Audio Models}, 
      author={Hui Wang and Cheng Liu and Junyang Chen and Haoze Liu and Yuhang Jia and Shiwan Zhao and Jiaming Zhou and Haoqin Sun and Hui Bu and Yong Qin},
      year={2025},
      eprint={2509.02398},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2509.02398}, 
}
```
## Acknowledgements
We thank the following projects:
- Audiobox Aesthetics: https://github.com/facebookresearch/audiobox-aesthetics
- CLAP: https://github.com/microsoft/CLAP
