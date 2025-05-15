import os
import logging
from pathlib import Path

from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    # Program base config
    ABSOLUTE_BASE_PATH: Path = Path(__file__).resolve().parent.parent
    STORAGE_PATH: Path = ABSOLUTE_BASE_PATH / "storage"

    # Server config
    LOG_LEVEL: str = "INFO"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8900
    SERVER_API_TOKEN: str | None = None
    IS_PRODUCTION: bool = False

    # minio 配置
    MINIO_HOST: str
    MINIO_PORT: str
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
    MYSQL_DB_NAME: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ensure_directories()

    def ensure_directories(self):
        for path in [
            self.STORAGE_PATH,
        ]:
            path.mkdir(parents=True, exist_ok=True)
