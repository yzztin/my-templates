from keycloak import KeycloakOpenID
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from configs.config import Config

config = Config()


def get_keycloak_(token):
    try:
        client_secret = ""
        if token.startswith("Bearer "):
            client_secret = token[7:]
        keycloak_openid = KeycloakOpenID(
            server_url=config.KEYCLOAK_SERVER_URL,
            client_id=config.KEYCLOAK_NOTION_CLIENT_ID,
            realm_name=config.KEYCLOAK_REALM_NAME,
            client_secret_key=client_secret,
        )
        token = keycloak_openid.token(grant_type="client_credentials")
        print(token)
    except Exception as e:
        print(e)
        return False
    return True


class OAuthKeyClockMiddleware(BaseHTTPMiddleware):
    auth_urls = ["paper", "attack", "vul", "hacker"]

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # 你可以在这里添加认证逻辑
        # 比如检查请求头中的令牌
        url_param = str(request.url).split("/")
        route_name = url_param[3]
        if route_name in self.auth_urls:
            token = request.headers.get("Authorization")
            if not token:
                return Response("无效的认证令牌", status_code=401)
            # todo keyclock 认证
            if not get_keycloak_(token):
                return Response("认证失败", status_code=401)
            # 如果认证通过，继续处理请求
        response = await call_next(request)
        return response
