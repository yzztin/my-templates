from dotenv import load_dotenv

from configs.base_config import BaseConfig
from configs.mysql_config import MysqlConfig

load_dotenv()

base_config = BaseConfig()
mysql_config = MysqlConfig()
