import logging

def setup_logging():
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    # 设置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 配置根日志记录器
    # logging.basicConfig(level=log_level, format=log_format)
    logging.basicConfig(level=log_level, format=log_format, force=True)

    # 设置第三方库特定的日志级别
    logging.getLogger("werkzeug").setLevel(log_level)