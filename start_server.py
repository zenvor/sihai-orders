#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四海订单处理工具 - Server 模式一键启动脚本

功能：
1. 自动创建和激活虚拟环境
2. 安装/更新依赖
3. 检查前端构建状态
4. 启动 Server 模式

使用方法：
    python start_server.py
    python start_server.py --host 0.0.0.0  # 允许局域网访问
    python start_server.py --port 9000     # 自定义端口
    python start_server.py --dev           # 开发模式
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import argparse
import shutil


class ServerLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.script_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.script_dir / "venv"
        self.frontend_dir = self.script_dir / "frontend"
        self.force_system_python = False

    def print_banner(self):
        """打印欢迎横幅"""
        print("=" * 60)
        print("🚀 四海订单处理工具 - Server 模式一键启动")
        print("=" * 60)
        print(f"📍 当前目录: {self.script_dir}")
        print(f"💻 操作系统: {platform.system()} {platform.release()}")
        print(f"🐍 Python版本: {sys.version.split()[0]}")
        print("=" * 60)

    def check_python_version(self):
        """检查Python版本"""
        print("🔍 检查 Python 版本...")
        if sys.version_info < (3, 7):
            print("❌ 错误: 需要 Python 3.7 或更高版本")
            print("请访问 https://www.python.org/downloads/ 下载最新版本")
            sys.exit(1)
        print(f"✅ Python 版本检查通过: {sys.version.split()[0]}")

    def get_python_executable(self):
        """获取Python可执行文件路径"""
        if self.force_system_python:
            return Path(sys.executable)
        if self.system == "windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"

    def create_virtual_environment(self):
        """创建虚拟环境"""
        if self.venv_dir.exists():
            print("✅ 虚拟环境已存在")
            return

        print("🔧 创建虚拟环境...")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_dir)],
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ 虚拟环境创建成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ 创建虚拟环境失败: {e}")
            if e.stderr:
                print(e.stderr)
            print("\n尝试使用系统 Python 运行...")
            self.force_system_python = True

    def install_dependencies(self):
        """安装依赖包"""
        print("📦 检查并安装依赖包...")
        requirements_file = self.script_dir / "requirements.txt"

        if not requirements_file.exists():
            print("❌ 找不到 requirements.txt 文件")
            sys.exit(1)

        python_exe = self.get_python_executable()

        try:
            print("   正在安装依赖...")
            subprocess.run(
                [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
                check=True,
                capture_output=True,
                text=True
            )
            subprocess.run(
                [str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)],
                check=True,
                capture_output=False,
                text=True
            )
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败: {e}")
            sys.exit(1)

    def check_frontend(self, dev_mode=False):
        """检查前端构建状态"""
        if dev_mode:
            print("🔥 开发模式：跳过前端构建检查")
            print("   请在另一个终端运行: cd frontend && npm run dev")
            return

        dist_dir = self.frontend_dir / "dist"

        if not dist_dir.exists():
            print("\n" + "=" * 60)
            print("⚠️  前端尚未构建")
            print("=" * 60)
            print("生产模式需要先构建前端，有以下选项：\n")
            print("选项 1: 自动构建前端（推荐）")
            print("选项 2: 手动构建")
            print("选项 3: 使用开发模式（前后端分离）\n")

            choice = input("请选择 [1/2/3]: ").strip()

            if choice == "1":
                self.build_frontend()
            elif choice == "2":
                print("\n请手动执行以下命令：")
                print("  cd frontend")
                print("  npm install")
                print("  npm run build")
                sys.exit(0)
            elif choice == "3":
                print("\n请按以下步骤操作：")
                print("1. 在终端 1 运行: python start_server.py --dev")
                print("2. 在终端 2 运行: cd frontend && npm run dev")
                print("3. 访问 http://localhost:5173")
                sys.exit(0)
            else:
                print("❌ 无效的选择")
                sys.exit(1)
        else:
            print("✅ 前端已构建")

    def build_frontend(self):
        """构建前端"""
        print("\n🏗️  开始构建前端...")

        # 检查 npm 是否安装
        if not shutil.which("npm"):
            print("❌ 未找到 npm，请先安装 Node.js")
            print("访问 https://nodejs.org/ 下载安装")
            sys.exit(1)

        # 检查 node_modules
        node_modules = self.frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 安装前端依赖...")
            try:
                subprocess.run(
                    ["npm", "install"],
                    cwd=str(self.frontend_dir),
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"❌ 前端依赖安装失败: {e}")
                sys.exit(1)

        # 构建前端
        print("🔨 构建前端...")
        try:
            subprocess.run(
                ["npm", "run", "build"],
                cwd=str(self.frontend_dir),
                check=True
            )
            print("✅ 前端构建完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 前端构建失败: {e}")
            sys.exit(1)

    def check_env_file(self):
        """检查环境变量配置"""
        env_file = self.script_dir / ".env"
        env_template = self.script_dir / "env.template"

        if not env_file.exists():
            print("\n⚠️  警告: 找不到 .env 文件")
            if env_template.exists():
                print("请复制 env.template 为 .env 文件，并配置您的 API 密钥")
            else:
                print("请创建 .env 文件并添加: DEEPSEEK_API_KEY=your_api_key")
            print("提示: 也可以在 Web 界面中配置 API Key")
        else:
            print("✅ .env 配置文件存在")

    def start_server(self, host="127.0.0.1", port=8000, dev=False):
        """启动服务器"""
        print("\n" + "=" * 60)
        print("🚀 启动服务器...")
        print("=" * 60)
        print(f"📍 监听地址: {host}:{port}")

        if dev:
            print("🔥 开发模式已启用（热重载）")

        print("\n" + "=" * 60)
        print("📖 访问方式:")
        print(f"   - API 文档: http://{host}:{port}/docs")
        print(f"   - Web 界面: http://{host}:{port}/")

        if host == "0.0.0.0":
            import socket
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
                print(f"   - 局域网访问: http://{local_ip}:{port}/")
            except:
                pass

        print("=" * 60)
        print("\n按 Ctrl+C 停止服务\n")
        print("=" * 60 + "\n")

        python_exe = self.get_python_executable()

        try:
            # 切换到项目目录
            os.chdir(self.script_dir)

            # 启动服务器
            cmd = [
                str(python_exe), "-m", "uvicorn",
                "backend.main:app",
                "--host", host,
                "--port", str(port)
            ]

            if dev:
                cmd.append("--reload")

            subprocess.run(cmd)

        except KeyboardInterrupt:
            print("\n\n👋 服务已停止")
        except Exception as e:
            print(f"\n❌ 启动服务器失败: {e}")
            sys.exit(1)

    def run(self, host="127.0.0.1", port=8000, dev=False):
        """主运行流程"""
        try:
            self.print_banner()
            self.check_python_version()
            self.create_virtual_environment()
            self.install_dependencies()
            self.check_env_file()
            self.check_frontend(dev_mode=dev)
            self.start_server(host=host, port=port, dev=dev)

        except KeyboardInterrupt:
            print("\n❌ 用户中断操作")
        except Exception as e:
            print(f"\n❌ 发生未知错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(
        description="四海订单处理工具 - Server 模式一键启动",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 默认启动（本地访问）
  python start_server.py

  # 允许局域网访问
  python start_server.py --host 0.0.0.0

  # 自定义端口
  python start_server.py --port 9000

  # 开发模式（热重载，需要单独启动前端）
  python start_server.py --dev
        """
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="监听地址 (默认: 127.0.0.1, 局域网访问使用 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="监听端口 (默认: 8000)"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="开发模式（启用热重载，需要单独启动前端）"
    )

    args = parser.parse_args()

    launcher = ServerLauncher()
    launcher.run(host=args.host, port=args.port, dev=args.dev)


if __name__ == "__main__":
    main()
