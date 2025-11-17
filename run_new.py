#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四海订单处理工具 - 统一启动脚本

支持两种模式:
1. CLI 模式: python run_new.py cli
2. Server 模式: python run_new.py server [--host HOST] [--port PORT] [--dev]
"""

import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='四海订单处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # CLI 模式（命令行处理）
  python run_new.py cli

  # Server 模式（启动 Web 服务）
  python run_new.py server

  # Server 模式（自定义端口）
  python run_new.py server --port 9000

  # Server 模式（开发模式，支持热重载）
  python run_new.py server --dev

  # Server 模式（允许局域网访问）
  python run_new.py server --host 0.0.0.0
        """
    )

    parser.add_argument(
        'mode',
        choices=['cli', 'server'],
        help='运行模式: cli (命令行) 或 server (Web 服务)'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Server 模式监听地址 (默认: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Server 模式端口 (默认: 8000)'
    )
    parser.add_argument(
        '--dev',
        action='store_true',
        help='开发模式（启用热重载）'
    )

    args = parser.parse_args()

    if args.mode == 'cli':
        # CLI 模式
        print("🖥️  启动 CLI 模式...")
        from cli.cli import run_cli
        run_cli()

    elif args.mode == 'server':
        # Server 模式
        print("🌐 启动 Server 模式...")
        print(f"📍 监听地址: {args.host}:{args.port}")

        if args.dev:
            print("🔥 开发模式已启用（热重载）")

        print("\n" + "="*60)
        print("📖 访问方式:")
        print(f"   - API 文档: http://{args.host}:{args.port}/docs")
        print(f"   - Web 界面: http://{args.host}:{args.port}/")
        if args.host == '0.0.0.0':
            import socket
            local_ip = socket.gethostbyname(socket.gethostname())
            print(f"   - 局域网访问: http://{local_ip}:{args.port}/")
        print("="*60 + "\n")

        try:
            import uvicorn
            uvicorn.run(
                "backend.main:app",
                host=args.host,
                port=args.port,
                reload=args.dev,
                log_level="info"
            )
        except ImportError:
            print("❌ 错误: 缺少 uvicorn 依赖")
            print("请安装: pip install uvicorn")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n👋 服务已停止")


if __name__ == "__main__":
    main()
