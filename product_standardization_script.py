#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四海订单处理工具 - CLI 入口脚本

此脚本复用 shared/product_standardizer.py 中的核心逻辑，
避免代码重复，确保 CLI 模式和 Web 模式使用相同的处理逻辑。
"""

import os
import sys
import glob
import logging
from dotenv import load_dotenv

# 确保可以导入 shared 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared.product_standardizer import ProductStandardizer

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_excel_file(directory: str = ".") -> str:
    """
    自动检测目录中的xlsx文件
    
    Args:
        directory: 要搜索的目录，默认为当前目录
        
    Returns:
        找到的Excel文件路径，如果没找到则返回None
    """
    # 搜索xlsx文件
    xlsx_files = glob.glob(os.path.join(directory, "*.xlsx"))
    
    if not xlsx_files:
        logger.error(f"在目录 {directory} 中未找到任何xlsx文件")
        return None
    elif len(xlsx_files) == 1:
        logger.info(f"找到Excel文件: {xlsx_files[0]}")
        return xlsx_files[0]
    else:
        # 如果有多个xlsx文件，优先选择包含"订单"、"模板"等关键词的文件
        priority_keywords = ["订单", "模板", "template", "order"]
        for keyword in priority_keywords:
            for file_path in xlsx_files:
                if keyword in os.path.basename(file_path).lower():
                    logger.info(f"找到优先Excel文件: {file_path}")
                    return file_path
        
        # 如果没有匹配关键词的，选择第一个
        logger.info(f"找到多个Excel文件，选择第一个: {xlsx_files[0]}")
        logger.info(f"所有找到的文件: {xlsx_files}")
        return xlsx_files[0]


def main():
    """CLI 主入口"""
    # 从环境变量获取 Deepseek API 密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        logger.error("请设置环境变量 DEEPSEEK_API_KEY")
        logger.error("可以创建 .env 文件并添加: DEEPSEEK_API_KEY=your_api_key")
        sys.exit(1)
    
    # 查找 Excel 文件
    excel_file = find_excel_file()
    if not excel_file:
        logger.error("无法找到Excel文件，处理终止")
        sys.exit(1)
    
    # 检查 order.txt 是否存在
    order_file = "order.txt"
    if not os.path.exists(order_file):
        logger.error(f"找不到订单文件: {order_file}")
        sys.exit(1)
    
    # 创建处理器实例并处理订单
    processor = ProductStandardizer(api_key=api_key)
    
    try:
        output_path = processor.process_order(order_file, excel_file)
        logger.info(f"处理完成，输出文件: {output_path}")
    except Exception as e:
        logger.error(f"处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
