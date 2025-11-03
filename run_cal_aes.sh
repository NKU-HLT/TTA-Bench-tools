#!/bin/bash
set -e

# Execute AES pipeline end-to-end
cd "$(dirname "$0")"

run_step() {
    local title="$1"; shift
    echo "=== ${title} ==="
    python "$@"
}

echo "=== Start AES pipeline ==="

run_step "Prepare AES input JSONL" cal_aes/1_prepare_input.py
run_step "Compute AES scores" cal_aes/2_cal_all_aes_score.py
run_step "Summarize mean AES" cal_aes/3_cal_mean_aes_score.py
run_step "Summarize attribute AES" cal_aes/6_cal_attr_aes_score.py

echo "AES pipeline finished."
