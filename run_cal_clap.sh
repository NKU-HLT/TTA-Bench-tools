#!/bin/bash
set -e

# Ensure running from script directory
cd "$(dirname "$0")"

echo "=== Start CLAP pipeline ==="

echo "Compute CLAP scores for all samples"
python cal_clap/4_cal_all_clap_score.py

echo "Summarize mean CLAP per system"
python cal_clap/5_cal_mean_clap_score.py

echo "Summarize attribute-level CLAP"
python cal_clap/7_cal_attr_clap_score.py

echo "CLAP pipeline finished."
