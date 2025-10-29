#!/bin/bash
set -e

# Get the directory of this script (absolute path)
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

python cal_fairness_score.py \
  --metric aes \
  --input "${BASE_DIR}/aes_results/aes_attribute_results.txt"

python cal_fairness_score.py \
  --metric clap \
  --input "${BASE_DIR}/clap_results/clap_attribute_results.txt"
