import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings:
    """应用配置"""

    def __init__(self):
        # 项目根目录
        self.base_dir = Path(__file__).parent.parent

        # Deepseek API 配置
        self.deepseek_api_key: Optional[str] = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_base_url: str = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

        # 文件存储路径
        self.upload_dir = self.base_dir / "uploads"
        self.output_dir = self.base_dir / "outputs"
        self.log_dir = self.base_dir / "logs"

        # 确保目录存在
        self.upload_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

        # 文件大小限制（50MB）
        self.max_file_size = 50 * 1024 * 1024

        # 任务超时时间（秒）
        self.task_timeout = 600  # 10分钟

        # 标准商品列表
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

        # CORS 配置
        # 允许所有来源（适合个人使用，如需限制请设置 ALLOW_CORS_ALL=false）
        self.allow_cors_all = os.getenv('ALLOW_CORS_ALL', 'true').lower() == 'true'

        # 默认允许的来源列表
        default_origins = [
            "http://localhost:5173",  # Vite 开发服务器
            "http://127.0.0.1:5173",
            "http://localhost:8000",  # 生产环境
            "http://127.0.0.1:8000",
            "http://localhost:3000",  # 备用端口
            "http://127.0.0.1:3000"
        ]

        # 从环境变量读取额外的允许来源（逗号分隔）
        extra_origins = os.getenv('CORS_ORIGINS', '').split(',')
        extra_origins = [origin.strip() for origin in extra_origins if origin.strip()]

        self.cors_origins = default_origins + extra_origins


# 全局配置实例
settings = Settings()
