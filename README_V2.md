# 四海订单处理工具 V2.0

> 支持 CLI 和 Server 双模式的订单处理工具

## ✨ 新特性

- 🖥️ **CLI 模式**: 保留原有的命令行处理功能
- 🌐 **Server 模式**: 全新的 Web 界面，操作更便捷
- 📦 **模块化设计**: 核心业务逻辑与界面解耦
- 🎨 **现代化 UI**: 基于 Vue 3 + Ant Design Vue
- 📊 **实时进度**: 实时显示处理进度和日志
- 🚀 **更易用**: 拖拽上传文件，一键处理

## 📋 快速开始

### ⚡ 一键启动（推荐）

**最简单的方式 - 使用一键启动脚本：**

- **Windows**: 双击 `start_server.bat`
- **Linux/macOS**: 运行 `./start_server.sh`
- **跨平台**: `python start_server.py`

脚本会自动：
- ✅ 创建虚拟环境
- ✅ 安装所有依赖
- ✅ 检查并构建前端（如需要）
- ✅ 启动 Server 模式

启动后访问 http://localhost:8000

**详细说明请查看 [QUICKSTART.md](QUICKSTART.md)**

---

### 📝 手动安装（高级用户）

#### 1. 安装依赖

**后端依赖**
```bash
pip install -r requirements.txt
```

**前端依赖**（仅 Server 模式需要）
```bash
cd frontend
npm install
```

#### 2. 配置 API Key

创建 `.env` 文件（从 `.env.template` 复制）：
```bash
cp env.template .env
```

编辑 `.env` 文件，添加你的 Deepseek API Key：
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3. 运行

**CLI 模式（命令行）**

```bash
# 确保 order.txt 和 Excel 模板在项目根目录
python run_new.py cli
```

**Server 模式（Web 界面）**

*开发模式*（前后端分离）：
```bash
# 终端 1: 启动后端
python run_new.py server --dev

# 终端 2: 启动前端
cd frontend
npm run dev

# 访问 http://localhost:5173
```

*生产模式*（一体化）：
```bash
# 1. 构建前端
cd frontend
npm run build
cd ..

# 2. 启动服务
python run_new.py server

# 访问 http://localhost:8000
```

*自定义配置*：
```bash
# 自定义端口
python run_new.py server --port 9000

# 允许局域网访问
python run_new.py server --host 0.0.0.0 --port 8000
```

## 📖 使用指南

### CLI 模式

1. 将订单数据保存到 `order.txt`
2. 准备好 Excel 模板文件（`.xlsx`）
3. 运行 `python run_new.py cli`
4. 等待处理完成，结果会直接更新到 Excel 文件

### Server 模式

1. 启动服务器
2. 打开浏览器访问 http://localhost:8000
3. 上传订单文件（order.txt）
4. 上传 Excel 模板
5. 点击「开始处理」
6. 实时查看处理进度
7. 处理完成后点击「下载结果」

## 🏗️ 项目结构

```
sihai-orders/
├── backend/              # 后端（FastAPI）
│   ├── main.py          # API 入口
│   ├── config.py        # 配置管理
│   └── task_manager.py  # 任务管理
├── frontend/            # 前端（Vue 3）
│   ├── src/
│   │   ├── App.vue      # 主组件
│   │   ├── components/  # 子组件
│   │   └── api/         # API 调用
│   └── package.json
├── shared/              # 共享模块
│   └── product_standardizer.py  # 核心业务逻辑
├── cli/                 # CLI 模式
│   └── cli.py          # CLI 入口
├── run_new.py          # 统一启动脚本
└── requirements.txt    # Python 依赖
```

## 🔧 API 接口

Server 模式提供以下 API 接口：

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/upload` | POST | 上传文件 |
| `/api/process` | POST | 开始处理任务 |
| `/api/task/{taskId}` | GET | 获取任务状态 |
| `/api/download/{taskId}` | GET | 下载结果 |
| `/api/config` | GET/POST | 配置管理 |
| `/docs` | GET | API 文档（Swagger UI） |

详细的 API 文档可以在启动服务后访问 http://localhost:8000/docs

## 🛠️ 开发

### 后端开发

```bash
# 启动开发服务器（热重载）
python run_new.py server --dev
```

### 前端开发

```bash
cd frontend
npm run dev
```

前端会自动代理 `/api` 请求到后端 `http://localhost:8000`。

### 构建前端

```bash
cd frontend
npm run build
```

构建产物会输出到 `frontend/dist/` 目录。

## 📝 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DEEPSEEK_API_KEY` | Deepseek API 密钥 | 无（必填） |
| `DEEPSEEK_BASE_URL` | Deepseek API 基础 URL | `https://api.deepseek.com` |

## ❓ 常见问题

### 1. 如何切换回旧版本？
旧版本的启动脚本仍然保留在 `run.py`，可以继续使用：
```bash
python run.py
```

### 2. Server 模式需要数据库吗？
不需要。任务状态存储在内存中，重启服务后会清空。

### 3. 可以同时运行多个任务吗？
可以。后端支持并发处理多个任务。

### 4. 上传的文件存储在哪里？
临时文件存储在 `uploads/` 目录，处理结果存储在 `outputs/` 目录。

### 5. 如何在局域网其他设备访问？
启动时使用 `--host 0.0.0.0` 参数：
```bash
python run_new.py server --host 0.0.0.0
```
然后在其他设备通过服务器的 IP 地址访问。

## 🔄 从 V1 迁移

如果你之前使用的是 V1 版本（`run.py`），现在可以：

1. **继续使用旧版本**: `python run.py`（完全兼容）
2. **迁移到新版本 CLI**: `python run_new.py cli`（功能相同）
3. **升级到 Server 模式**: `python run_new.py server`（推荐）

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
