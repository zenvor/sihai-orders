# CORS 跨域配置指南

## 默认配置

**默认情况下，Server 模式允许所有来源的跨域访问**，这适合：
- 个人使用
- 局域网访问
- 开发环境
- 快速部署

## 工作原理

启动服务时，你会看到以下日志：

```
INFO: CORS 配置: 允许所有来源访问
```

这意味着任何来源（包括局域网其他设备）都可以访问你的 API。

## 场景说明

### 场景 1: 个人使用（推荐，默认配置）

**不需要任何配置**，直接启动即可：

```bash
python start_server.py
```

支持：
- ✅ 本地访问 http://localhost:8000
- ✅ 局域网访问 http://192.168.x.x:8000
- ✅ 不同端口的前端开发服务器
- ✅ 浏览器扩展

### 场景 2: 局域网共享

启动时允许局域网访问：

```bash
python start_server.py --host 0.0.0.0
```

然后其他设备通过你的 IP 访问，例如：
- http://192.168.1.100:8000
- http://10.0.0.50:8000

**无需额外配置 CORS**，默认配置已经支持。

### 场景 3: 限制访问来源（生产环境）

如果你希望仅允许特定来源访问（例如部署到公网），编辑 `.env` 文件：

```bash
# 禁用允许所有来源
ALLOW_CORS_ALL=false

# 指定允许的来源（逗号分隔）
CORS_ORIGINS=http://example.com,https://example.com,http://192.168.1.100:8000
```

重启服务后，只有指定的来源可以访问。

## 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ALLOW_CORS_ALL` | `true` | 是否允许所有来源访问 |
| `CORS_ORIGINS` | 空 | 额外允许的来源列表（逗号分隔） |

### 配置示例

#### 1. 默认配置（推荐）

`.env` 文件：
```bash
DEEPSEEK_API_KEY=sk-xxxxx
# CORS 使用默认配置，允许所有来源
```

#### 2. 仅允许特定域名

`.env` 文件：
```bash
DEEPSEEK_API_KEY=sk-xxxxx

# 限制访问来源
ALLOW_CORS_ALL=false
CORS_ORIGINS=https://myapp.com,https://www.myapp.com
```

#### 3. 允许特定 IP 和端口

`.env` 文件：
```bash
DEEPSEEK_API_KEY=sk-xxxxx

ALLOW_CORS_ALL=false
CORS_ORIGINS=http://192.168.1.100:8000,http://192.168.1.101:8000,http://localhost:3000
```

## 常见问题

### Q1: 我在局域网其他设备访问时提示跨域错误？

A: 检查以下几点：
1. 确认 `.env` 中 `ALLOW_CORS_ALL=true`（默认配置）
2. 启动时使用 `--host 0.0.0.0` 参数
3. 检查防火墙是否允许端口访问

### Q2: 我需要部署到公网，如何保护安全？

A: 建议：
1. 设置 `ALLOW_CORS_ALL=false`
2. 在 `CORS_ORIGINS` 中只添加你的域名
3. 考虑添加身份验证机制
4. 使用 HTTPS

### Q3: 开发模式前端和后端分离时的跨域问题？

A: **不需要担心**，默认配置已经支持：
- 前端开发服务器（http://localhost:5173）
- 后端 API 服务器（http://localhost:8000）

### Q4: 如何验证 CORS 配置是否生效？

A: 启动服务时查看日志：

```bash
# 允许所有来源
INFO: CORS 配置: 允许所有来源访问

# 限制来源
INFO: CORS 配置: 仅允许以下来源 ['http://example.com', ...]
```

### Q5: 可以同时允许所有来源和指定来源吗？

A: 不可以，两者二选一：
- `ALLOW_CORS_ALL=true`: 允许所有来源（忽略 CORS_ORIGINS）
- `ALLOW_CORS_ALL=false`: 仅允许 CORS_ORIGINS 中指定的来源

## 安全建议

### 个人使用/开发环境
- ✅ 使用默认配置（`ALLOW_CORS_ALL=true`）
- ✅ 仅在本地或可信局域网运行

### 生产环境/公网部署
- ⚠️ 设置 `ALLOW_CORS_ALL=false`
- ⚠️ 明确指定允许的来源
- ⚠️ 启用 HTTPS
- ⚠️ 考虑添加身份验证
- ⚠️ 使用反向代理（Nginx/Caddy）

## 调试 CORS 问题

### 1. 检查浏览器控制台

打开浏览器开发者工具（F12），查看 Console 和 Network 标签页，查找 CORS 相关错误信息。

### 2. 检查服务端日志

查看服务启动时的 CORS 配置日志：

```bash
python start_server.py
```

### 3. 测试 API 访问

使用 curl 测试（不受 CORS 限制）：

```bash
curl http://localhost:8000/api/health
```

如果 curl 能访问但浏览器不能，就是 CORS 问题。

### 4. 临时禁用浏览器 CORS 检查（仅用于测试）

**Chrome（仅限测试）：**
```bash
# Windows
chrome.exe --disable-web-security --user-data-dir="C:\temp\chrome_dev"

# macOS
open -na "Google Chrome" --args --disable-web-security --user-data-dir="/tmp/chrome_dev"

# Linux
google-chrome --disable-web-security --user-data-dir="/tmp/chrome_dev"
```

⚠️ **警告**：仅用于调试，不要用此模式浏览其他网站。

## 总结

对于本项目（个人使用场景）：
- ✅ **无需配置**，默认支持所有跨域访问
- ✅ 支持本地和局域网访问
- ✅ 开发和生产模式都能正常工作
- ✅ 如需限制访问，编辑 `.env` 文件即可

如有疑问，请参考 [README_V2.md](README_V2.md) 或提交 Issue。
