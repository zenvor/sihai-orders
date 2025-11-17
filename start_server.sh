#!/bin/bash
# 四海订单处理工具 - Server 模式一键启动脚本 (Linux/macOS)

echo "=========================================="
echo "🚀 四海订单处理工具 - Server 模式"
echo "=========================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

# 运行 Python 启动脚本
python3 start_server.py "$@"
