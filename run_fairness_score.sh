#!/bin/bash
set -e

# Get the directory of this script (absolute path)
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Start fairness scoring (MOS) ==="
python "${BASE_DIR}/cal_fairness_score.py" \
  --input "${BASE_DIR}/subjective_results/attr_result_common.txt" \
  --output "${BASE_DIR}/subjective_results/fs_result_mos.txt"

echo "Fairness scoring (MOS) finished."
