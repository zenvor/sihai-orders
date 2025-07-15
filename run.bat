@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 四海订单处理工具 - Windows启动脚本
echo ========================================
echo.
echo 提示：如果遇到权限问题，请右键选择"以管理员身份运行"
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    echo 安装完成后请重新运行此脚本
    exit /b 1
)

echo Python环境检查通过
echo.

echo 启动订单处理程序...
echo.

REM 运行Python启动脚本
python run.py

echo.
echo 程序执行完毕