from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from configs import BASE_CONFIG


class BearerTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_paths: list[str] | None = None):
        """
        默认使用 apps 目录下的文件夹作为需要 token 校验的路由前缀
        """
        super().__init__(app)
        self.token = BASE_CONFIG.SERVER_API_TOKEN
        self.protected_paths = protected_paths or self.get_app_router_paths()

    async def dispatch(self, request: Request, call_next):
        # 如果未设置 token，则跳过校验，直接放行
        if not self.token:
            return await call_next(request)

        path = request.url.path

        # 只对指定路径前缀进行校验
        if any(path.startswith(p) for p in self.protected_paths):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise PermissionError("Missing or invalid Authorization header")

            bearer_token = auth_header[len("Bearer ") :].strip()

            if bearer_token != self.token:
                raise PermissionError("Wrong token")

        return await call_next(request)

    @classmethod
    def get_app_router_paths(cls):
        """
        读取 apps 目录下的所有文件夹名称
        """
        app_path = BASE_CONFIG.ABSOLUTE_BASE_PATH / "apps"
        return ["/" + f.name for f in app_path.iterdir() if f.is_dir()]
