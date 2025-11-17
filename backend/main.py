from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
from pathlib import Path
import uuid
from typing import Optional
import logging

from .task_manager import TaskManager
from .config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="四海订单处理 API",
    description="订单数据处理和商品标准化 API",
    version="2.0.0"
)

# CORS 配置
# 根据配置决定是否允许所有来源（适合个人使用）
if settings.allow_cors_all:
    # 允许所有来源（推荐用于个人使用、开发和局域网访问）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS 配置: 允许所有来源访问")
else:
    # 仅允许指定来源（用于生产环境）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS 配置: 仅允许以下来源 {settings.cors_origins}")

# 初始化任务管理器
task_manager = TaskManager()

# 生产环境：挂载前端静态文件
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    logger.info("前端静态文件已挂载")


@app.get("/")
async def serve_frontend():
    """提供前端页面（生产环境）"""
    index_file = frontend_dist / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    else:
        return {
            "message": "四海订单处理 API",
            "version": "2.0.0",
            "docs": "/docs",
            "frontend": "请先构建前端: cd frontend && npm run build"
        }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "message": "四海订单处理服务运行正常",
        "version": "2.0.0"
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件（order.txt 或 Excel 模板）

    Args:
        file: 上传的文件

    Returns:
        文件信息
    """
    # 验证文件类型
    if not (file.filename.endswith('.txt') or file.filename.endswith('.xlsx')):
        raise HTTPException(
            status_code=400,
            detail="只支持 .txt 或 .xlsx 文件"
        )

    # 验证文件大小
    file.file.seek(0, 2)  # 移动到文件末尾
    file_size = file.file.tell()
    file.file.seek(0)  # 重置到文件开头

    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制 ({settings.max_file_size / 1024 / 1024}MB)"
        )

    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    save_path = settings.upload_dir / f"{file_id}{file_ext}"

    # 保存文件
    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"文件上传成功: {file.filename} -> {save_path}")

        return {
            "fileId": file_id,
            "filename": file.filename,
            "size": file_size,
            "path": str(save_path)
        }

    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@app.post("/api/process")
async def start_processing(
    order_file_id: str = Query(..., description="订单文件ID"),
    excel_file_id: str = Query(..., description="Excel模板文件ID"),
    api_key: Optional[str] = Query(None, description="Deepseek API Key (可选)")
):
    """
    开始处理任务

    Args:
        order_file_id: 订单文件ID
        excel_file_id: Excel模板文件ID
        api_key: Deepseek API Key（可选，如果不提供则使用配置中的）

    Returns:
        任务ID
    """
    # 查找文件
    order_file = settings.upload_dir / f"{order_file_id}.txt"
    excel_file = settings.upload_dir / f"{excel_file_id}.xlsx"

    if not order_file.exists():
        raise HTTPException(status_code=404, detail="订单文件不存在")

    if not excel_file.exists():
        raise HTTPException(status_code=404, detail="Excel模板文件不存在")

    # 使用配置中的 API Key 或传入的 API Key
    used_api_key = api_key or settings.deepseek_api_key
    if not used_api_key:
        raise HTTPException(
            status_code=400,
            detail="请配置 Deepseek API Key（通过环境变量或请求参数）"
        )

    # 创建任务
    try:
        task_id = task_manager.create_task(
            order_file=str(order_file),
            excel_file=str(excel_file),
            api_key=used_api_key
        )

        logger.info(f"任务已创建: {task_id}")

        return {
            "taskId": task_id,
            "message": "任务已启动"
        }

    except Exception as e:
        logger.error(f"创建任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@app.get("/api/task/{task_id}")
async def get_task_status(task_id: str):
    """
    获取任务状态

    Args:
        task_id: 任务ID

    Returns:
        任务状态信息
    """
    task = task_manager.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        "taskId": task_id,
        "status": task["status"],
        "progress": task["progress"],
        "message": task["message"],
        "logs": task.get("logs", []),
        "createdAt": task.get("created_at"),
        "result": task.get("result")
    }


@app.get("/api/tasks")
async def get_all_tasks():
    """
    获取所有任务列表

    Returns:
        任务列表
    """
    tasks = task_manager.get_all_tasks()
    return {
        "tasks": tasks,
        "count": len(tasks)
    }


@app.get("/api/download/{task_id}")
async def download_result(task_id: str):
    """
    下载处理结果

    Args:
        task_id: 任务ID

    Returns:
        Excel文件
    """
    task = task_manager.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="任务尚未完成")

    result_file = task.get("result")
    if not result_file or not Path(result_file).exists():
        raise HTTPException(status_code=404, detail="结果文件不存在")

    return FileResponse(
        result_file,
        filename=f"订单处理结果_{task_id[:8]}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.delete("/api/task/{task_id}")
async def delete_task(task_id: str):
    """
    删除任务

    Args:
        task_id: 任务ID

    Returns:
        删除结果
    """
    success = task_manager.delete_task(task_id)

    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        "message": "任务已删除",
        "taskId": task_id
    }


@app.get("/api/config")
async def get_config():
    """
    获取配置信息

    Returns:
        配置信息
    """
    return {
        "hasApiKey": bool(settings.deepseek_api_key),
        "standardProducts": settings.standard_products,
        "maxFileSize": settings.max_file_size,
        "taskTimeout": settings.task_timeout
    }


@app.post("/api/config")
async def update_config(api_key: Optional[str] = Query(None)):
    """
    更新配置

    Args:
        api_key: Deepseek API Key

    Returns:
        更新结果
    """
    if api_key:
        settings.deepseek_api_key = api_key
        logger.info("API Key 已更新")

    return {
        "success": True,
        "message": "配置已更新"
    }


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("="*60)
    logger.info("🚀 四海订单处理服务已启动")
    logger.info(f"📍 上传目录: {settings.upload_dir}")
    logger.info(f"📍 输出目录: {settings.output_dir}")
    logger.info(f"🔑 API Key 配置: {'已配置' if settings.deepseek_api_key else '未配置'}")
    logger.info("="*60)


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("👋 四海订单处理服务已关闭")
