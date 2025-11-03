#!/bin/bash
set -e

echo "=== Start MOS pipeline ==="

echo "Preprocess raw MOS CSVs"
python cal_mos/1_process.py

echo "Compute mean MOS → subjective_results/result_*.txt"
python cal_mos/2_cal_mean_mos.py

echo "Compute attribute MOS → subjective_results/attr_result_*.txt"
python cal_mos/3_cal_attr_mos.py

echo "MOS pipeline finished."

