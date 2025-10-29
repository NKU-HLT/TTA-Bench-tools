#!/bin/bash

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# 执行 Python 模块
run_step() {
    local step_name="$1"
    local module_path="$2"

    echo "=== 开始: ${step_name} ==="
    python -m "${module_path}"
    if [ $? -ne 0 ]; then
        echo "[错误] ${step_name} 执行失败！"
        exit 1
    fi
    echo "=== 完成: ${step_name} ==="
}

echo "=== 开始 AES 全流程 ==="

run_step "准备 AES 输入文件" "cal_aes.1_prepare_input"
run_step "计算 AES 分数" "cal_aes.2_calculate_aes"
run_step "汇总系统平均 AES 分数" "cal_aes.summarize_mean_aes"
run_step "汇总属性级 AES 分数" "cal_aes.summarize_attribute_aes"

echo "✅ AES 评估流程完成！"
