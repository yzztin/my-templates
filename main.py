import logging

from apps.create_app import create_app
from apps.xxx.router import router as xxx_router
from configs import BASE_CONFIG


app = create_app()

app.include_router(xxx_router, prefix="/xxx")

logger = logging.getLogger(__name__)


@app.get("/ping")
def ping():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    logger.info(f"启动服务: {BASE_CONFIG.SERVER_HOST}:{BASE_CONFIG.SERVER_PORT}")

    uvicorn.run(
        app,
        host=BASE_CONFIG.SERVER_HOST,
        port=BASE_CONFIG.SERVER_PORT,
        reload=False,
    )
