#!/bin/bash
set -e

# Robustness evaluation
cd "$(dirname "$0")"

echo "=== Start robustness scoring ==="
python cal_robustness_score.py
echo "Robustness scoring finished."
