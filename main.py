import logging

from apps.create_app import create_app
from apps.xxx.router import router as xxx_router
from configs import base_config


app = create_app()

app.include_router(xxx_router, prefix="/xxx")

logger = logging.getLogger(__name__)


@app.get("/ping")
def ping():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    logger.info(f"启动服务: {base_config.SERVER_HOST}:{base_config.SERVER_PORT}")

    uvicorn.run(
        app,
        host=base_config.SERVER_HOST,
        port=base_config.SERVER_PORT,
        reload=False,
    )
