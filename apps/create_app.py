from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from configs.log import setup_logger, setup_logger_to_file
from configs import BASE_CONFIG
from utils.exceptions import ExceedRateLimitException


def create_app(lifespan=None) -> FastAPI:
    # 初始化日志
    setup_logger()
    # setup_logger_to_file("service")

    if BASE_CONFIG.IS_PRODUCTION:
        docs_url = None
        redoc_url = None
    else:
        docs_url = "/docs"
        redoc_url = "/redoc"

    app = FastAPI(
        title="",
        description="",
        docs_url=docs_url,
        redoc_url=redoc_url,
        lifespan=lifespan,
    )

    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=["*"],  # 在生产环境中，应该限制为特定的源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 定义异常处理，遇到异常时，fastapi 接口会返回对应的错误信息
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        match exc:
            case PermissionError():
                return JSONResponse(status_code=403, content={"msg": "权限拒绝", "detail": str(exc)})
            case FileNotFoundError():
                return JSONResponse(status_code=404, content={"msg": "文件未找到", "detail": str(exc)})
            case ValueError():
                return JSONResponse(status_code=400, content={"msg": "无效输入", "detail": str(exc)})
            case TimeoutError():
                return JSONResponse(status_code=408, content={"msg": "请求超时"})
            case _:
                return JSONResponse(status_code=500, content={"msg": "服务器内部错误"})

    return app