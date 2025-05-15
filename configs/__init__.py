from dotenv import load_dotenv

from configs.base_config import BaseConfig
from configs.mysql_config import MysqlConfig

load_dotenv()

BASE_CONFIG = BaseConfig()
MYSQL_CONFIG = MysqlConfig()  # type: ignore
