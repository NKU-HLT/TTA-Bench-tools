#!/bin/bash
set -e

# Fairness evaluation for AES and CLAP
cd "$(dirname "$0")"

echo "=== Start fairness scoring ==="

python cal_fairness_score.py \
	--metric aes \
	--input "$(pwd)/aes_results/aes_attribute_results.txt"

python cal_fairness_score.py \
	--metric clap \
	--input "$(pwd)/clap_results/clap_attribute_results.txt"

echo "Fairness scoring finished."
