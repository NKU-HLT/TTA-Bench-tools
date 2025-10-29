
# 📦 TTA-Bench-tools

> This repo is used for calculating and analyzing scores result for [TTA-Bench: A comprehensive benchmark for text-to-audio generation evaluation](https://jiusansan222.github.io/tta-bench/).

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2501.12345-b31b1b.svg)](https://jiusansan222.github.io/tta-bench/)
[![Project Page](https://img.shields.io/badge/Project-Website-blue.svg)](https://jiusansan222.github.io/tta-bench/)


---

## 📖 Overview

Text-to-Audio (TTA) generation has made rapid progress, but current evaluation methods remain narrow, focusing mainly on perceptual quality while overlooking robustness, generalization, and ethical concerns. We present TTA-Bench, a comprehensive benchmark for evaluating TTA models across functional performance, reliability, and social responsibility. It covers seven dimensions including accuracy, robustness, fairness, and toxicity, and includes 2,999 diverse prompts generated through automated and manual methods. We introduce a unified evaluation protocol that combines objective metrics with over 118,000 human annotations from both experts and general users. Ten state-of-the-art models are benchmarked under this framework, offering detailed insights into their strengths and limitations. TTA-Bench establishes a new standard for holistic and responsible evaluation of TTA systems. The dataset, evaluation tools, and results are available at [TTA-Bench](https://jiusansan222.github.io/tta-bench).

---

## 🚀 Getting Started

### 0. Clone the repository

```bash
git clone https://github.com/NKU-HLT/TTA-Bench-tools.git
cd ./TTA-Bench-tools
```
### 1. Prepare input in Audiobox-aesthetic style & Calculate AES scores

```bash
bash cal_aes_pipeline.sh
```

这会自动执行：

- 1_prepare_input.py：生成输入列表

- 2_cal_all_aes_score.py：调用 audio-aes 工具计算分数

- 3_cal_mean_aes_score.py：计算各维度内总平均分

- 6_cal_attr_aes_score.py：计算各维度内各属性平均分

### 2. Calculate CLAP scores

```bash
bash run_cal_clap.sh
```

这会自动执行：

- 4_cal_all_clap_score.py：基于ms-clap计算所有音频的CLAP分数

- 5_cal_mean_clap_score.py：计算各维度内总CLAP平均分

- 7_cal_attr_clap_score.py：计算各维度内各属性平均分


### 3. Calculate MOS (Mean Opinion Scores)

```bash
bash run_cal_clap.sh
```

这会自动执行：
- 1_process.py：标注数据预处理

- 2_cal_mean_mos.py：计算各维度内总MOS平均分

- 3_cal_attr_mos.py：计算各维度内各属性MOS平均分

## 🙏 Acknowledgements

We would like to thank the following projects that made this work possible:

- [Audiobox-aesthetic](https://github.com/facebookresearch/audiobox-aesthetics)
- [CLAP](https://github.com/microsoft/CLAP)
