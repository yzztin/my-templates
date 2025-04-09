import logging
import os.path
from logging.handlers import RotatingFileHandler

from configs import base_config


def setup_logger():
    """
    最简单的日志配置，日志信息直接输出到终端
    """
    log_level = getattr(logging, base_config.LOG_LEVEL.upper(), logging.INFO)

    # 设置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 配置根日志记录器
    # logging.basicConfig(level=log_level, format=log_format)
    logging.basicConfig(level=log_level, format=log_format, force=True)

    # 设置第三方库特定的日志级别
    logging.getLogger("werkzeug").setLevel(log_level)
    

def setup_logger_to_file():
    """
    设置日志记录到文件
    """
    log_level = getattr(logging, base_config.LOG_LEVEL.upper(), logging.INFO)

    # 设置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # 创建一个文件处理器，并设置日志文件的最大大小和备份数量
    file_name = os.path.join(base_config.STORAGE_PATH, "xxx.log")
    file_handler = RotatingFileHandler(
        filename=file_name,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,  # 最多保留5个备份
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)

    # 将文件处理器添加到日志记录器
    logger.addHandler(file_handler)
