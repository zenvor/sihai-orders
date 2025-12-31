import uuid
from threading import Thread
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
import shutil
import logging

from shared.product_standardizer import ProductStandardizer

logger = logging.getLogger(__name__)


class TaskManager:
    """简单的任务管理器（基于内存存储）"""

    def __init__(self):
        self.tasks: Dict[str, dict] = {}

    def create_task(self, order_file: str, excel_file: str, api_key: str) -> str:
        """
        创建并启动任务

        Args:
            order_file: 订单文件路径
            excel_file: Excel模板文件路径
            api_key: Deepseek API Key

        Returns:
            任务ID
        """
        task_id = str(uuid.uuid4())

        # 复制 Excel 文件到输出目录（避免修改原文件）
        output_file = Path("outputs") / f"{task_id}.xlsx"
        shutil.copy(excel_file, output_file)

        task = {
            "id": task_id,
            "status": "pending",  # pending, processing, completed, failed
            "progress": 0,
            "message": "等待处理...",
            "logs": [],
            "created_at": datetime.now().isoformat(),
            "order_file": order_file,
            "excel_file": excel_file,
            "output_file": str(output_file),
            "result": None
        }

        self.tasks[task_id] = task

        # 在后台线程中处理
        thread = Thread(target=self._process_task, args=(task_id, api_key), daemon=True)
        thread.start()

        logger.info(f"任务已创建: {task_id}")
        return task_id

    def get_task(self, task_id: str) -> Optional[dict]:
        """
        获取任务信息

        Args:
            task_id: 任务ID

        Returns:
            任务信息字典，如果任务不存在则返回 None
        """
        return self.tasks.get(task_id)

    def _process_task(self, task_id: str, api_key: str):
        """
        处理任务（在后台线程中运行）

        Args:
            task_id: 任务ID
            api_key: Deepseek API Key
        """
        task = self.tasks[task_id]

        def progress_callback(percent: int, message: str):
            """进度回调函数"""
            # 详细日志：只添加日志，不更新进度和状态
            if percent == -2:
                log_entry = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "message": message,
                    "type": "detail"
                }
                task["logs"].append(log_entry)
                return

            task["progress"] = percent
            task["message"] = message

            # 添加日志
            log_entry = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": message,
                "percent": percent
            }
            task["logs"].append(log_entry)

            # 更新状态
            if percent == 100:
                task["status"] = "completed"
            elif percent == -1:
                task["status"] = "failed"
            elif percent > 0:
                task["status"] = "processing"

            logger.info(f"[任务 {task_id[:8]}] [{percent}%] {message}")

        try:
            # 创建处理器
            processor = ProductStandardizer(
                api_key=api_key,
                progress_callback=progress_callback
            )

            # 处理订单
            result_path = processor.process_order(
                order_file_path=task["order_file"],
                excel_file_path=task["output_file"]
            )

            task["result"] = str(result_path)
            task["status"] = "completed"
            logger.info(f"任务完成: {task_id}")

        except Exception as e:
            task["status"] = "failed"
            task["message"] = f"处理失败: {str(e)}"
            task["logs"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": f"❌ 错误: {str(e)}",
                "percent": -1
            })
            logger.error(f"任务失败: {task_id}, 错误: {e}", exc_info=True)

    def get_all_tasks(self) -> list:
        """获取所有任务列表"""
        return list(self.tasks.values())

    def delete_task(self, task_id: str) -> bool:
        """
        删除任务

        Args:
            task_id: 任务ID

        Returns:
            是否删除成功
        """
        if task_id in self.tasks:
            # 清理输出文件
            task = self.tasks[task_id]
            if task.get("result"):
                result_file = Path(task["result"])
                if result_file.exists():
                    result_file.unlink()

            del self.tasks[task_id]
            logger.info(f"任务已删除: {task_id}")
            return True

        return False
