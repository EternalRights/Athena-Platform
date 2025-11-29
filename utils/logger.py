# utils/logger.py
import logging
import os
from datetime import datetime


class Logger:
    """日志工具类"""

    def __init__(self, name="WebAutomation", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """设置日志处理器"""
        # 创建logs目录
        log_dir = "reports/logs/"
        os.makedirs(log_dir, exist_ok=True)

        # 文件处理器
        log_filename = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """信息日志"""
        self.logger.info(message)

    def warning(self, message):
        """警告日志"""
        self.logger.warning(message)

    def error(self, message):
        """错误日志"""
        self.logger.error(message)

    def debug(self, message):
        """调试日志"""
        self.logger.debug(message)