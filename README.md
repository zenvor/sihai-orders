# 四海订单处理工具 🚀

自动处理订单数据，把订单信息填入Excel表格。

## 🚀 怎么使用？

### 第一步：准备文件
1. 确保文件夹里有 `order.txt`（订单数据）
2. 确保文件夹里有 Excel 表格文件（.xlsx格式）
3. 配置API密钥：
   - 复制 `env.template` 文件为 `.env`
   - 在 `.env` 文件中将 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 替换为你的真实 Deepseek API 密钥
   - 如果没有API密钥，请到 [Deepseek官网](https://platform.deepseek.com/) 注册获取

### 第二步：运行程序
**Windows用户**：
- 双击 `run.bat` 文件
- 如果提示安全警告，点击"运行"
- 如果无法运行，右键选择"以管理员身份运行"

**Mac用户**：
- 双击 `run.sh` 文件
- 如果提示"无法打开"或权限问题，打开终端执行：
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

### 第三步：等待完成
程序会自动处理数据并更新Excel文件，完成后按回车键退出。

## 📝 order.txt 文件格式

```
店铺名称1:
商品名称1:数量1件
商品名称2:数量2件

店铺名称2:
商品名称3:数量3件
商品名称4:数量4件
```

## ❓ 遇到问题？

**提示"找不到Python"**
- 需要先安装Python，去 [python.org](https://www.python.org/downloads/) 下载安装

**Mac权限问题**
- 如果双击无法运行，在终端执行：`chmod +x run.sh && ./run.sh`
- 或者右键点击 `run.sh`，选择"打开"

**Windows权限问题**
- 右键选择"以管理员身份运行"
- 如果提示执行策略限制，在PowerShell中执行：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**程序运行出错**
- 检查 `order.txt` 文件格式是否正确
- 检查Excel文件是否存在
- 确保网络连接正常

---

**就这么简单！** 🎉