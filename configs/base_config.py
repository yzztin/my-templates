import os
import logging

from h11 import SERVER
from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    # Program base config
    ABSOLUTE_BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STORAGE_PATH: str = os.path.join(ABSOLUTE_BASE_PATH, "storage")
    LOG_LEVEL: str = "INFO"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # minio 配置
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str

    # mongodb 配置
    MONGO_HOST: str
    MONGO_PORT: str
    MONGO_DB_NAME: str
    MONGO_USER: str
    MONGO_PASSWORD: str

    # mysql 配置
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB_NAME_PLUGIN: str
    # MYSQL_DB_NAME_AIGC: str
