#!/bin/bash

# 确保脚本在自身目录执行
cd "$(dirname "$0")"

echo "=== 开始 CLAP 全流程 ==="

# 1.
echo "=== 计算所有音频样本的 CLAP 分数 ==="
python cal_clap/4_cal_all_clap_score.py

# 2. 
echo "=== 汇总系统平均 CLAP 分数 ==="
python cal_clap/5_cal_mean_clap_score.py

# 3.
echo "=== 汇总属性级 CLAP 分数 ==="
python cal_clap/7_cal_attr_clap_score.py

echo "✅ CLAP 评估流程完成！"
