from urllib.parse import quote_plus

from configs.base_config import BaseConfig


class MysqlConfig(BaseConfig):
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return (
            f"mysql+pymysql://"
            f"{quote_plus(self.MYSQL_USER)}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB_NAME_PLUGIN}"
        )

    @property
    def SQLALCHEMY_URI_WITHOUT_DATABASE(self):
        return (
            f"mysql+pymysql://"
            f"{quote_plus(self.MYSQL_USER)}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}"
        )
