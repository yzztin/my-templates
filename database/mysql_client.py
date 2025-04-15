import logging

from flask_sqlalchemy import SQLAlchemy

from configs import config, MYSQL_CONFIG

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def init_db(app):
    """
    初始化数据库连接，创建数据表
    :param app:
    :return:
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_CONFIG.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)

    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        logger.exception(f"数据库初始化失败: {e}")


def create_database():
    try:
        from sqlalchemy import create_engine, text

        engine = create_engine(MYSQL_CONFIG.SQLALCHEMY_URI_WITHOUT_DATABASE, echo=True)
        with engine.connect() as conn:
            create_sql = f"CREATE DATABASE IF NOT EXISTS `{config.MYSQL_DB_NAME_PLUGIN}`"
            conn.execute(text(create_sql))
            logger.info(f"数据库 {config.MYSQL_DB_NAME_PLUGIN} 已创建")

    except Exception as e:
        logger.exception(f"创建数据库 {config.MYSQL_DB_NAME_PLUGIN} 失败: {e}")
