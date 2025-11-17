# 🚀 快速开始 - Server 模式

## 一键启动（推荐）

### Windows
双击运行 `start_server.bat` 或在命令行中：
```cmd
start_server.bat
```

### Linux / macOS
```bash
./start_server.sh
# 或
bash start_server.sh
```

### 跨平台（Python）
```bash
python start_server.py
```

## 首次运行

脚本会自动：
1. ✅ 检查 Python 版本
2. ✅ 创建虚拟环境（venv/）
3. ✅ 安装所有依赖
4. ✅ 检查前端构建状态
5. ✅ 启动 Server 模式

**如果前端未构建**，脚本会提示你选择：
- 选项 1: 自动构建前端（推荐，需要安装 Node.js）
- 选项 2: 手动构建
- 选项 3: 使用开发模式（前后端分离）

## 配置 API Key

### 方法 1: 环境变量（推荐）
1. 复制 `env.template` 为 `.env`
2. 编辑 `.env`，填入你的 API Key：
   ```
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
   ```

### 方法 2: Web 界面配置
启动服务后，在 Web 界面的「设置」中配置 API Key。

## 访问

启动成功后，浏览器访问：
- **Web 界面**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

### 局域网访问

**已自动配置好跨域访问**，无需额外设置！

1. 启动时使用 `--host 0.0.0.0`：
   ```bash
   python start_server.py --host 0.0.0.0
   ```

2. 在其他设备（手机、平板、其他电脑）访问：
   ```
   http://你的IP地址:8000
   例如：http://192.168.1.100:8000
   ```

3. 查看你的 IP 地址：
   - Windows: `ipconfig`
   - Linux/macOS: `ifconfig` 或 `ip addr`

**详细的跨域配置说明请查看 [CORS.md](CORS.md)**

## 高级选项

### 自定义端口
```bash
python start_server.py --port 9000
```

### 允许局域网访问
```bash
python start_server.py --host 0.0.0.0
```
然后其他设备通过你的 IP 地址访问，例如：http://192.168.1.100:8000

### 开发模式（热重载）
```bash
# 终端 1
python start_server.py --dev

# 终端 2
cd frontend
npm run dev
```
访问 http://localhost:5173

## 停止服务

按 `Ctrl + C` 停止服务。

## 常见问题

### Q: Python 版本过低？
A: 需要 Python 3.7+，请访问 https://python.org 下载最新版本。

### Q: 端口被占用？
A: 使用 `--port` 参数更换端口：
```bash
python start_server.py --port 9000
```

### Q: 前端构建失败？
A: 确保已安装 Node.js 16+，然后手动构建：
```bash
cd frontend
npm install
npm run build
```

### Q: 虚拟环境有问题？
A: 删除 venv 目录后重新运行：
```bash
rm -rf venv  # Linux/macOS
# 或
rmdir /s venv  # Windows

python start_server.py
```

## 旧版本 CLI 模式

如果你想使用命令行模式：
```bash
python run_new.py cli
```

或继续使用旧版本：
```bash
python run.py
```
