#!/bin/bash

# 设置脚本目录为工作目录
cd "$(dirname "$0")"

echo "========================================"
echo "四海订单处理工具 - macOS/Linux启动脚本"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未找到Python，请先安装Python 3.7或更高版本"
        echo "macOS用户可以通过以下方式安装:"
        echo "1. 访问 https://www.python.org/downloads/"
        echo "2. 或使用Homebrew: brew install python"
        read -p "按回车键退出..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "使用Python命令: $PYTHON_CMD"
echo "启动订单处理程序..."
echo

# 运行Python启动脚本
$PYTHON_CMD run.py

echo
echo "程序执行完毕"
read -p "按回车键退出..."