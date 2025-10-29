#!/bin/bash

set -e  # 遇到错误立即退出

echo "=== 开始 CLAP 全流程 ==="

# 1.
echo "=== 原始MOS数据预处理 ==="
python cal_mos/1_process.py

# 2.
echo "=== 计算系统平均MOS → subjective_results/result_*.txt"
python cal_mos/2_cal_mean_mos.py

# 3.
echo "=== 计算属性MOS → subjective_results/attr_result_*.txt"
python cal_mos/3_cal_attr_mos.py


echo "✅ MOS 评估流程完成！"

