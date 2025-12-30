# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

**四海订单处理工具** 是一个 Python 自动化脚本，用于处理电商订单数据并将其填入 Excel 表格。该工具使用 Deepseek AI 对商品名称进行智能标准化和映射。

**项目类型**：Python 脚本工具
**支持平台**：Windows、macOS
**Python 版本**：3.7+

## 快速开发命令

### 运行应用程序
```bash
# 一键启动（自动处理虚拟环境和依赖）
python run.py

# 或使用平台特定脚本
./run.sh          # macOS/Linux
run.bat           # Windows
```

### 虚拟环境管理
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

# 安装依赖
pip install -r requirements.txt

# 生成依赖清单（修改依赖后运行）
pip freeze > requirements.txt
```

### 测试和调试
```bash
# 直接运行核心脚本（跳过启动器逻辑）
python product_standardization_script.py

# 运行时加载调试信息
python -u run.py
```

## 代码架构

### 核心文件结构

```
sihai-orders/
├── run.py                              # 启动器脚本，处理虚拟环境和依赖安装
├── product_standardization_script.py   # 核心业务逻辑
├── requirements.txt                    # Python 依赖清单
├── .env.template                       # 环境变量配置模板
├── .env                                # 实际配置文件（gitignored）
├── .gitignore                          # Git 忽略规则
├── order.txt                           # 输入：订单数据文件
├── 订单模板.xlsx.template              # 输入：Excel 模板
└── run.sh / run.bat                    # 平台特定的启动脚本
```

### 主要模块

#### 1. **run.py** - OrderProcessorLauncher 类 (306 行)
**职责**：环境初始化和脚本启动

**关键方法**：
- `check_python_version()` - 验证 Python 3.7+
- `setup_virtual_environment()` - 创建和激活虚拟环境
- `install_dependencies()` - 安装 requirements.txt 中的依赖
- `validate_required_files()` - 检查必需的输入文件（order.txt、.xlsx）
- `launch_main_script()` - 启动核心脚本

**关键特性**：
- 支持多种 Python 环境（虚拟环境、系统 Python、--target 安装）
- 处理 Windows 组策略限制（无法使用虚拟环境时自动切换）
- 跨平台执行（Windows、macOS、Linux）
- 详细的错误处理和用户友好的提示

#### 2. **product_standardization_script.py** - ProductStandardizer 类 (533 行)
**职责**：订单数据处理和 AI 驱动的商品标准化

**核心业务流程**：
1. `read_order_data_from_file()` - 读取 order.txt 文件
2. `parse_raw_data()` - 解析店铺名称和商品信息
3. `normalize_product_name()` - 格式化商品名称
4. `extract_all_product_variants()` - 提取所有商品变体（用于 AI 学习）
5. `create_product_mapping()` - **调用 Deepseek API**，使用 AI 进行智能商品映射
6. `standardize_data()` - 标准化整个数据集
7. `write_to_excel()` - 将结果写入 Excel 文件

**标准商品列表**：
```python
self.standard_products = [
    "四海170g鱼蛋鲜装",
    "四海150g鱼之豆腐鲜装",
    "四海250g手打香菇贡丸鲜装",
    "四海170g八爪鱼味鱼球鲜装",
    "四海250g手打牛筋丸鲜装",
    "四海250g手打牛肉丸鲜装",
    "四海200g鲜装鱼籽虾饼",
    "四海170g鲜装台湾花枝味鱼丸",
    "四海170g鲜装墨鱼味鱼丸",
    "四海250g墨鱼鱼饼",
    "四海150g鲜装牛肉丸"
]
```

### 数据流程

```
order.txt (输入)
    ↓
OrderProcessorLauncher (run.py)
    ├─ 环境检查和虚拟环境设置
    ├─ 依赖安装
    └─ 启动 ProductStandardizer
        ↓
    ProductStandardizer (product_standardization_script.py)
        ├─ 读取订单数据
        ├─ 解析店铺和商品信息
        ├─ 调用 Deepseek API 进行 AI 映射
        └─ 标准化和匹配商品
            ↓
        Excel 文件 (输出)
```

## 外部依赖

| 库 | 用途 |
|----|----|
| **pandas** | 数据处理和 Excel 操作 |
| **openpyxl** | Excel 文件读写 |
| **openai** | Deepseek API 客户端（兼容 OpenAI SDK） |
| **requests** | HTTP 请求（备选方案） |
| **python-dotenv** | 环境变量加载（从 .env 读取 API 密钥） |

## 配置管理

### 环境变量
所有敏感信息通过 `.env` 文件管理（不提交到 Git）：

```bash
# .env 文件格式
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 文件约定
- `order.txt` - 固定输入文件名，格式：
  ```
  店铺名称1:
  商品名称1:数量1件
  商品名称2:数量2件

  店铺名称2:
  商品名称3:数量3件
  ```

- `*.xlsx` - 自动识别文件夹中的 Excel 文件作为输出目标

## 代码风格指南

遵循全局 CLAUDE.md 规范（/Users/claude/.claude/CLAUDE.md）：

- **命名**：
  - 文件/文件夹：kebab-case（如 run.py、product_standardization_script.py）
  - 常量：camelCase（apiKey、maxRetryCount）
  - 类名：PascalCase（ProductStandardizer）
  - 函数：snake_case（read_order_data_from_file）

- **注释**：使用中文，说明"为什么"而非"做什么"
- **异步处理**：使用 async/await（已应用于 API 调用）
- **错误处理**：在关键操作和 API 调用处使用 try-catch，错误信息中文化

## 扩展和修改指南

### 添加新的标准商品
编辑 `product_standardization_script.py` 中 `ProductStandardizer.__init__()` 方法的 `standard_products` 列表。

### 修改 API 提示词
在 `create_product_mapping()` 方法中修改发送给 Deepseek 的提示词（system_prompt）。

### 支持新的 Excel 格式
在 `write_to_excel()` 方法中添加新的列名和数据映射逻辑。

### 集成不同的 AI 提供商
替换 `ProductStandardizer.__init__()` 中的 OpenAI 客户端初始化和 API 调用（但保持相同的接口）。

## 常见问题和边界情况

### 已处理的问题

1. **Windows 组策略限制**（run.py）
   - 问题：某些企业环境禁用虚拟环境脚本
   - 解决：自动切换到 `--target` 方式安装依赖或系统 Python

2. **跨平台兼容性**
   - 支持 Windows、macOS、Linux
   - 自动检测平台并使用相应的命令

3. **缺失依赖**
   - 自动检测并安装 requirements.txt 中的依赖
   - 支持备选安装方法

### 需要改进的地方

- 考虑添加单元测试（特别是数据解析和 AI 映射逻辑）
- 添加更详细的 API 错误处理和重试机制
- 支持配置文件指定输入/输出文件路径
- 添加日志输出到文件，便于故障排查

## 开发工作流

1. **修改代码**：编辑 `.py` 文件
2. **测试**：运行 `python run.py` 或直接调用相关方法
3. **提交**：遵循 Conventional Commits 格式
   ```bash
   git add .
   git commit -m "feat(product): 添加新的商品标准化规则"
   ```
4. **更新依赖**：`pip freeze > requirements.txt`

## 相关文档

- README.md - 用户指南和使用说明
- .env.template - 环境变量配置示例
- Deepseek API 文档：https://platform.deepseek.com/
