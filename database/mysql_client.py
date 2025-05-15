import logging
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from configs import BASE_CONFIG, MYSQL_CONFIG

logger = logging.getLogger(__name__)

# 声明 Base，用于后续模型继承
Base = declarative_base()

# 初始化为空，稍后由 init_db() 设置
engine = None
SessionLocal = None


def init_db():
    """
    初始化数据库连接与表结构
    """
    global engine, SessionLocal

    try:
        # 创建数据库引擎
        engine = create_engine(
            MYSQL_CONFIG.SQLALCHEMY_DATABASE_URI,
            echo=False,
            future=True,
        )
        # 创建会话工厂
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # 创建所有模型对应的表
        Base.metadata.create_all(bind=engine)

        logger.info("数据库初始化完成")

    except Exception as e:
        logger.exception(f"数据库初始化失败: {e}")


def create_database():
    """
    创建数据库（如果不存在）
    """
    try:
        temp_engine = create_engine(MYSQL_CONFIG.SQLALCHEMY_URI_WITHOUT_DATABASE, echo=True, future=True)
        with temp_engine.connect() as conn:
            create_sql = f"CREATE DATABASE IF NOT EXISTS `{BASE_CONFIG.MYSQL_DB_NAME}`"
            conn.execute(text(create_sql))
            logger.info(f"数据库 {BASE_CONFIG.MYSQL_DB_NAME} 已创建")
    except Exception as e:
        logger.exception(f"创建数据库 {BASE_CONFIG.MYSQL_DB_NAME} 失败: {e}")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # type: ignore
    try:
        yield db
    finally:
        db.close()