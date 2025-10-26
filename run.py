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
import tempfile
import urllib.request

class OrderProcessorLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.script_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.script_dir / "venv"
        self.main_script = self.script_dir / "product_standardization_script.py"
        self.force_system_python = False  # 组策略阻止虚拟环境时切换
        self.deps_target_dir = self.script_dir / ".deps"  # --target 安装目录
        
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
        if self.force_system_python:
            return Path(sys.executable)
        if self.system == "windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
            
    def get_pip_executable(self):
        """获取pip可执行文件路径"""
        if self.force_system_python:
            # 当强制使用系统 Python 时，优先通过 python -m pip 调用，此方法仅保留兼容
            return Path(sys.executable)
        if self.system == "windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"

    def is_group_policy_block_error(self, error: Exception) -> bool:
        """判断是否为 Windows 组策略阻止（WinError 1260）。"""
        msg = str(error) if error else ""
        winerr = getattr(error, "winerror", None)
        if winerr == 1260:
            return True
        if "组策略阻止" in msg or "blocked by group policy" in msg.lower():
            return True
        return False
            
    def ensure_pip(self):
        """确保虚拟环境中 pip 可用且为最新版本（Windows 兼容）。"""
        python_exe = self.get_python_executable()
        # 先检查 python 可执行文件是否存在
        if not python_exe.exists():
            print("❌ 未找到虚拟环境的 Python 可执行文件，请尝试删除 venv 目录后重试")
            sys.exit(1)

        # 检查 pip 是否可用
        try:
            subprocess.run([str(python_exe), "-m", "pip", "--version"],
                           check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("🔧 未检测到 pip，尝试使用 ensurepip 安装...")
            try:
                subprocess.run([str(python_exe), "-m", "ensurepip", "--upgrade"],
                               check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ ensurepip 执行失败: {e}")
                # 兜底：尝试使用官方 get-pip.py 引导安装
                print("🔁 尝试通过 get-pip.py 引导安装 pip...")
                try:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        get_pip_path = Path(tmp_dir) / "get-pip.py"
                        url = "https://bootstrap.pypa.io/get-pip.py"
                        urllib.request.urlretrieve(url, get_pip_path)
                        subprocess.run([str(python_exe), str(get_pip_path)],
                                       check=True, capture_output=False, text=True)
                except Exception as e2:
                    print(f"❌ get-pip.py 引导失败: {e2}")
                    print("请确认网络允许访问 https://bootstrap.pypa.io 或联系管理员安装 pip/ensurepip")
                    sys.exit(1)

        # 升级 pip / setuptools / wheel，避免新版本 Python 的兼容性问题
        print("   升级 pip/setuptools/wheel...")
        try:
            subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade",
                            "pip", "setuptools", "wheel"],
                           check=True, capture_output=False, text=True)
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ pip 升级失败（可忽略）: {e}")
            # 不立即退出，部分环境下升级失败但基础功能可用
            
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
            if e.stderr:
                print(e.stderr)
            print("尝试使用 --without-pip 回退创建虚拟环境...")
            try:
                subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(self.venv_dir)],
                               check=True, capture_output=True, text=True)
                print("✅ 虚拟环境创建成功（未包含 pip，将在后续步骤中引导安装）")
            except subprocess.CalledProcessError as e2:
                print(f"❌ 回退创建虚拟环境仍失败: {e2}")
                if e2.stderr:
                    print(e2.stderr)
                print("请确保已安装 Python 的 venv/ensurepip 模块，或尝试：")
                print("1) 重新安装官方 Python（勾选 pip/venv）")
                print("2) 将项目移动到不包含括号与特殊字符的路径（如 C:\\sihai-orders）")
                print("3) 删除项目下 venv 目录后重试")
                sys.exit(1)
            
    def install_dependencies(self):
        """安装依赖包"""
        print("📦 检查并安装依赖包...")
        requirements_file = self.script_dir / "requirements.txt"

        def install_with_active_python():
            python_exe = self.get_python_executable()
            self.ensure_pip()
            if requirements_file.exists():
                print("   从 requirements.txt 安装依赖...")
                subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)],
                               check=True, capture_output=False, text=True)
            else:
                minimal_packages = ["pandas", "openpyxl", "openai", "requests", "python-dotenv"]
                for package in minimal_packages:
                    print(f"   安装 {package}...")
                    subprocess.run([str(python_exe), "-m", "pip", "install", package],
                                   check=True, capture_output=False, text=True)

        def install_with_system_python_user():
            print("   以系统 Python 和 --user 安装依赖...")
            args = [sys.executable, "-m", "pip", "install", "--user"]
            if requirements_file.exists():
                args += ["-r", str(requirements_file)]
            else:
                args += ["pandas", "openpyxl", "openai", "requests", "python-dotenv"]
            subprocess.run(args, check=True, capture_output=False, text=True)

        def install_with_system_python_target():
            print(f"   使用 --target 安装到 {self.deps_target_dir} ...")
            self.deps_target_dir.mkdir(parents=True, exist_ok=True)
            args = [sys.executable, "-m", "pip", "install", "--no-warn-script-location", "--target", str(self.deps_target_dir)]
            if requirements_file.exists():
                args += ["-r", str(requirements_file)]
            else:
                args += ["pandas", "openpyxl", "openai", "requests", "python-dotenv"]
            subprocess.run(args, check=True, capture_output=False, text=True)

        try:
            try:
                install_with_active_python()
                return
            except OSError as e:
                if self.is_group_policy_block_error(e):
                    print("⚠️  检测到组策略阻止虚拟环境可执行文件，切换到系统 Python 模式安装依赖")
                    self.force_system_python = True
                else:
                    raise
            except subprocess.CalledProcessError as e:
                # 有些情况下调用成功但内部仍因策略失败
                if "组策略阻止" in str(e) or "blocked by group policy" in str(e).lower():
                    print("⚠️  检测到组策略阻止虚拟环境执行，切换到系统 Python 模式安装依赖")
                    self.force_system_python = True
                else:
                    raise

            # 使用系统 Python 的回退方案
            try:
                install_with_system_python_user()
            except subprocess.CalledProcessError:
                print("   --user 安装失败，尝试 --target 到项目目录下的 .deps ...")
                install_with_system_python_target()

        except FileNotFoundError as e:
            print(f"   ❌ 执行 pip 时出错（可能的原因：pip 不存在或路径包含非法字符）: {e}")
            print("   处理建议：删除项目下 venv 目录后重新运行，或手动执行 `python -m venv venv` 再运行此脚本")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"   ❌ 依赖安装失败: {e}")
            print("   请检查网络连接、代理设置，或稍后重试")
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
            
        # 检查环境变量配置文件
        env_file = self.script_dir / ".env"
        env_template = self.script_dir / "env.template"
        
        if not env_file.exists():
            if env_template.exists():
                print("⚠️  警告: 找不到.env文件")
                print("请复制env.template为.env文件，并配置您的API密钥")
            else:
                print("⚠️  警告: 找不到环境变量配置文件")
                print("请创建.env文件并添加: DEEPSEEK_API_KEY=your_api_key")
        else:
            print("✅ .env配置文件存在")
            
    def run_main_script(self):
        """运行主脚本"""
        print("🚀 启动订单处理程序...")
        print("="*60)
        
        python_exe = self.get_python_executable()
        
        try:
            # 切换到脚本目录
            os.chdir(self.script_dir)
            
            # 运行主脚本
            env = os.environ.copy()
            if self.deps_target_dir.exists():
                env["PYTHONPATH"] = (str(self.deps_target_dir) + os.pathsep + env.get("PYTHONPATH", ""))
            result = subprocess.run([str(python_exe), str(self.main_script)], 
                                  text=True, capture_output=False, env=env)
            
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