from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from configs.log import setup_logger
from utils.exceptions import ExceedRateLimitException


def create_app() -> FastAPI:
    # 初始化日志
    setup_logger()

    app = FastAPI(
        title="xxxx API 接口服务",
        description="提供 xxxx 功能",
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
            case FileNotFoundError():
                return JSONResponse(status_code=404, content={"detail": str(exc)})
            case ValueError():
                return JSONResponse(status_code=400, content={"detail": "无效输入"})
            case TimeoutError():
                return JSONResponse(status_code=408, content={"detail": "请求超时"})
            case ExceedRateLimitException():
                return JSONResponse(status_code=429, content={"detail": str(exc)})
            case _:
                return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})

    return app