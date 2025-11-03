#!/bin/bash
set -e

# Robustness evaluation using MOS subjective results
cd "$(dirname "$0")"

echo "=== Start robustness scoring (MOS) ==="
python cal_robustness_score.py

echo "Robustness scoring (MOS) finished."