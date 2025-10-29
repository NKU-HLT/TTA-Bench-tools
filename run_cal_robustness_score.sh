
#!/bin/bash

# 执行鲁棒性评估流程的脚本

echo "开始执行鲁棒性评估流程..."

# 确保脚本在正确目录执行
cd "$(dirname "$0")"

# 计算鲁棒性分数
echo "步骤1: 计算鲁棒性分数..."
python cal_robustness_score.py

echo "鲁棒性评估流程完成！"
