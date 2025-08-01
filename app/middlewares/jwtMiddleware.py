from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
from app.utils.baseResponse import BaseResponse

class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.publicEndpoint = getattr(settings, 'PUBLIC_ENDPOINTS', [])

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.publicEndpoint):
            return self.get_response(request)

        requestHeader = request.headers.get("Authorization")
        if not requestHeader or not requestHeader.startswith("Bearer "):
            return BaseResponse.custom(status_code=status.HTTP_401_UNAUTHORIZED, message="Thiếu token")

        accessTokenSplit = requestHeader.split(" ")[1]
        try:
            token = AccessToken(accessTokenSplit)
            user_id = token.get("user_id")
            if not user_id:
                return BaseResponse.custom(status_code=status.HTTP_401_UNAUTHORIZED, message="Token không hợp lệ")
            request.user_id = user_id
        except (TokenError, InvalidToken):
            return BaseResponse.custom(status_code=status.HTTP_401_UNAUTHORIZED, message="Token không hợp lệ", data="invalid_token")
        return self.get_response(request)
        