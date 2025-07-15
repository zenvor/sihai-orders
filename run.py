#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四海订单处理工具 - 一键启动脚本
支持 Windows 和 macOS 系统

使用方法：
1. 双击运行此脚本
2. 或在终端中运行：python run.py
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

class OrderProcessorLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.script_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.script_dir / "venv"
        self.main_script = self.script_dir / "product_standardization_script.py"
        
    def print_banner(self):
        """打印欢迎横幅"""
        print("="*60)
        print("🚀 四海订单处理工具 - 一键启动")
        print("="*60)
        print(f"📍 当前目录: {self.script_dir}")
        print(f"💻 操作系统: {platform.system()} {platform.release()}")
        print(f"🐍 Python版本: {sys.version.split()[0]}")
        print("="*60)
        
    def check_python_version(self):
        """检查Python版本"""
        print("🔍 检查Python版本...")
        if sys.version_info < (3, 7):
            print("❌ 错误: 需要Python 3.7或更高版本")
            print("请访问 https://www.python.org/downloads/ 下载最新版本")
            sys.exit(1)
        print(f"✅ Python版本检查通过: {sys.version.split()[0]}")
        
    def get_python_executable(self):
        """获取Python可执行文件路径"""
        if self.system == "windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
            
    def get_pip_executable(self):
        """获取pip可执行文件路径"""
        if self.system == "windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"
            
    def create_virtual_environment(self):
        """创建虚拟环境"""
        if self.venv_dir.exists():
            print("✅ 虚拟环境已存在")
            return
            
        print("🔧 创建虚拟环境...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], 
                         check=True, capture_output=True, text=True)
            print("✅ 虚拟环境创建成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ 创建虚拟环境失败: {e}")
            print("请确保已安装Python的venv模块")
            sys.exit(1)
            
    def install_dependencies(self):
        """安装依赖包"""
        print("📦 检查并安装依赖包...")
        
        # 必需的包列表
        required_packages = [
            "pandas",
            "openpyxl", 
            "openai",
            "requests"
        ]
        
        pip_exe = self.get_pip_executable()
        
        for package in required_packages:
            print(f"   安装 {package}...")
            try:
                subprocess.run([str(pip_exe), "install", package], 
                             check=True, capture_output=True, text=True)
                print(f"   ✅ {package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ {package} 安装失败: {e}")
                print("请检查网络连接或手动安装依赖")
                sys.exit(1)
                
    def check_required_files(self):
        """检查必需文件"""
        print("📋 检查必需文件...")
        
        # 检查主脚本
        if not self.main_script.exists():
            print(f"❌ 找不到主脚本: {self.main_script}")
            sys.exit(1)
        print("✅ 主脚本文件存在")
        
        # 检查order.txt文件
        order_file = self.script_dir / "order.txt"
        if not order_file.exists():
            print("⚠️  警告: 找不到order.txt文件")
            print("请确保order.txt文件在同一目录下")
        else:
            print("✅ order.txt文件存在")
            
        # 检查Excel文件
        excel_files = list(self.script_dir.glob("*.xlsx"))
        if not excel_files:
            print("⚠️  警告: 找不到Excel模板文件(.xlsx)")
            print("请确保Excel模板文件在同一目录下")
        else:
            print(f"✅ 找到Excel文件: {[f.name for f in excel_files]}")
            
    def run_main_script(self):
        """运行主脚本"""
        print("🚀 启动订单处理程序...")
        print("="*60)
        
        python_exe = self.get_python_executable()
        
        try:
            # 切换到脚本目录
            os.chdir(self.script_dir)
            
            # 运行主脚本
            result = subprocess.run([str(python_exe), str(self.main_script)], 
                                  text=True, capture_output=False)
            
            print("="*60)
            if result.returncode == 0:
                print("✅ 程序执行完成！")
            else:
                print(f"❌ 程序执行出错，退出码: {result.returncode}")
                
        except Exception as e:
            print(f"❌ 运行主脚本时出错: {e}")
            
    def run(self):
        """主运行流程"""
        try:
            self.print_banner()
            self.check_python_version()
            self.create_virtual_environment()
            self.install_dependencies()
            self.check_required_files()
            self.run_main_script()
            
        except KeyboardInterrupt:
            print("\n❌ 用户中断操作")
        except Exception as e:
            print(f"\n❌ 发生未知错误: {e}")

if __name__ == "__main__":
    launcher = OrderProcessorLauncher()
    launcher.run()