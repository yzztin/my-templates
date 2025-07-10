import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.create_app import create_app
from apps.example.router.examble_router import router as example_router
from configs import BASE_CONFIG
from database.mysql_client import init_db, create_database
from middlewares.token_verify import BearerTokenMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化数据库
    await create_database()
    await init_db()
    yield

app = create_app(lifespan=lifespan)


app.include_router(example_router, prefix="/example")
app.add_middleware(BearerTokenMiddleware)

logger = logging.getLogger(__name__)


@app.get("/ping")
def ping():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    logger.info(f"启动服务: {BASE_CONFIG.model_dump()}")

    uvicorn.run(
        app,
        host=BASE_CONFIG.SERVER_HOST,
        port=BASE_CONFIG.SERVER_PORT,
        reload=False,
    )
