from channels.middleware import BaseMiddleware
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from app.services.accountsService import AccountsService

@database_sync_to_async
def get_user_from_token(token: str):
    try:
        decoded = jwt_decode(
            token,
            key=settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
            algorithms=[settings.SIMPLE_JWT.get("ALGORITHM", "HS256")],
        )
        return AccountsService.find_by_id(decoded["user_id"])
    except Exception:
        return AnonymousUser()
    
class WsJwtMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        try:
            user = await get_user_from_token(token)
            scope["user"] = user
        except Exception:
            scope["user"] = AnonymousUser()
        return await super().__call__(scope, receive, send)
