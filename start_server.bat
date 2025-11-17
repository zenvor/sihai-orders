@echo off
REM 四海订单处理工具 - Server 模式一键启动脚本 (Windows)

echo ==========================================
echo 🚀 四海订单处理工具 - Server 模式
echo ==========================================

REM 检查 Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 python
    echo 请先安装 Python 3.7 或更高版本
    pause
    exit /b 1
)

REM 运行 Python 启动脚本
python start_server.py %*

pause
