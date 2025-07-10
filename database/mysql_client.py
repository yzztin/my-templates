import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from configs import BASE_CONFIG, MYSQL_CONFIG

logger = logging.getLogger(__name__)

# 声明 Base，用于后续模型继承
Base = declarative_base()

# 创建数据库引擎
engine = create_async_engine(MYSQL_CONFIG.SQLALCHEMY_DATABASE_URI, echo=True, future=True)
# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    """
    初始化数据库连接与表结构
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("数据库初始化完成")

    except Exception as e:
        logger.exception(f"数据库初始化失败: {e}")


async def create_database():
    """
    创建数据库（如果不存在）
    """
    try:
        temp_engine = create_engine(MYSQL_CONFIG.SQLALCHEMY_URI_WITHOUT_DATABASE)
        with temp_engine.connect() as conn:
            create_sql = f"CREATE DATABASE IF NOT EXISTS `{BASE_CONFIG.MYSQL_DB_NAME}`"
            conn.execute(text(create_sql))
            conn.commit()

            logger.info(f"数据库 {BASE_CONFIG.MYSQL_DB_NAME} 已创建")
    except Exception as e:
        logger.exception(f"创建数据库 {BASE_CONFIG.MYSQL_DB_NAME} 失败: {e}")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db_session:
        yield db_session
