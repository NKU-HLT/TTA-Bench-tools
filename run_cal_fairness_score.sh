
#!/bin/bash

# 执行公平性评估流程的脚本
# 包括计算AES和CLAP的公平性分数

echo "开始执行公平性评估流程..."

# 确保脚本在正确目录执行
cd "$(dirname "$0")"

# 1. 计算AES公平性分数
echo "步骤1: 计算AES公平性分数..."
python cal_fairness_score_aes.py

# 2. 计算CLAP公平性分数
echo "步骤2: 计算CLAP公平性分数..."
python cal_fairness_score_clap.py

echo "公平性评估流程完成！"
