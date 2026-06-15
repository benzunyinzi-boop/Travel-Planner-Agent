"""
日志配置模块
提供统一的日志配置和追踪ID生成
"""

import logging
import sys
import uuid
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

# 日志目录
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / f"travel_planner_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logging(log_level=logging.INFO):
    """
    配置应用程序日志系统
    
    Args:
        log_level: 日志级别，默认INFO
    """
    # 创建日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 清除已有的处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    return root_logger


def generate_trace_id():
    """生成唯一的追踪ID"""
    return str(uuid.uuid4())[:8]


class TraceIDFilter(logging.Filter):
    """为日志记录添加trace_id字段"""
    
    def __init__(self, trace_id=None):
        super().__init__()
        self.trace_id = trace_id or generate_trace_id()
    
    def filter(self, record):
        record.trace_id = self.trace_id
        return True


def get_logger(name, trace_id=None):
    """
    获取带追踪ID的日志记录器
    
    Args:
        name: 日志记录器名称
        trace_id: 追踪ID，如果为None则自动生成
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 添加trace_id过滤器
    trace_filter = TraceIDFilter(trace_id)
    logger.addFilter(trace_filter)
    
    return logger


# 初始化日志系统
setup_logging()
