#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 模式 - 命令行订单处理

保留原有的命令行处理功能
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.product_standardizer import ProductStandardizer

# 加载环境变量
load_dotenv()


def run_cli():
    """运行 CLI 模式"""
    print("="*60)
    print("🚀 四海订单处理工具 - CLI 模式")
    print("="*60)

    # 获取 API Key
    api_key = os.getenv('DEEPSEEK_API_KEY')

    if not api_key:
        print("❌ 错误: 请设置环境变量 DEEPSEEK_API_KEY")
        print("可以创建 .env 文件并添加: DEEPSEEK_API_KEY=your_api_key")
        sys.exit(1)

    # 查找文件
    order_file = project_root / "order.txt"
    if not order_file.exists():
        print(f"❌ 错误: 找不到订单文件 {order_file}")
        sys.exit(1)

    # 查找 Excel 文件
    excel_files = list(project_root.glob("*.xlsx"))
    if not excel_files:
        print("❌ 错误: 找不到 Excel 模板文件 (.xlsx)")
        sys.exit(1)

    excel_file = excel_files[0]
    print(f"📄 订单文件: {order_file.name}")
    print(f"📊 Excel 文件: {excel_file.name}")
    print("="*60)

    # 创建处理器并处理订单
    try:
        def progress_callback(percent, message):
            """进度回调"""
            print(f"[{percent:3d}%] {message}")

        processor = ProductStandardizer(
            api_key=api_key,
            progress_callback=progress_callback
        )

        # 处理订单
        result_path = processor.process_order(
            order_file_path=str(order_file),
            excel_file_path=str(excel_file)
        )

        print("="*60)
        print(f"✅ 处理完成！结果已保存到: {result_path}")
        print("="*60)

    except Exception as e:
        print("="*60)
        print(f"❌ 处理失败: {e}")
        print("="*60)
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
