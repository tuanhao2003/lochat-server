from rest_framework.views import APIView
from rest_framework import status
from app.services.accountsService import AccountsService
from app.mapping.accountsMapping import AccountsMapping
from app.utils.baseResponse import BaseResponse
from app.utils.dictHelper import DictHelper

class AccountsController(APIView):

    def post(self, request, action = None):
        try:
            if action and action == "search":
                data = str(request.data.get("search_data"))
                if data:
                    result = None
                    if "@" in data and "." in data and data.count("@") == 1:
                        result = AccountsService.find_by_email(data)
                        if not result:
                            result = AccountsService.find_by_nickname(data)
                    else:
                        result = AccountsService.find_by_nickname(data)
                    if result:
                        if isinstance(result, list):
                            return BaseResponse.success(data=AccountsMapping(result, many=True).data)
                        return BaseResponse.success(data=AccountsMapping(result).data)
                    return BaseResponse.not_found(message="Không tìm thấy tài khoản")
                return BaseResponse.custom(status_code=status.HTTP_400_BAD_REQUEST,message="Thông tin tìm kiếm không hợp lệ")
            
            if action and action == "login":
                username = str(request.data.get("username"))
                email = str(request.data.get("email"))
                password = str(request.data.get("password"))
                if (username or email) and password:
                    result = AccountsService.login(request.data)
                    if result:
                        return BaseResponse.success(data=result)
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Sai tài khoản hoặc mật khẩu")
                return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Thiếu thông tin đăng nhập")
            
            if action and action == "registry":
                username = request.data.get("username")
                nickname = request.data.get("nickname")
                email = request.data.get("email")
                password = request.data.get("password")
                birth = request.data.get("birth")

                if all([username, nickname, email, password, birth]):
                    result = AccountsService.registry(DictHelper.parse_python_dict(AccountsMapping(data=request.data)))
                    if result:
                        return BaseResponse.success(data=AccountsMapping(result).data)
                    return BaseResponse.custom(status.HTTP_400_BAD_REQUEST, "Đăng ký thất bại")
                return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Thiếu thông tin đăng ký")
            
            if action and action == "restock_token":
                headerAuth = str(request.headers.get("Authorization"))
                if not headerAuth or not headerAuth.startswith("Bearer "):
                    token = headerAuth.split(" ")[1]
                    if token:
                        result = AccountsService.restock_token(token)
                        if result:
                            return BaseResponse.success(data=result)
                        return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Token không hợp lệ")
                return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Thiếu token")
            
            return BaseResponse.internal(message=str(e))
        except Exception as e:
            return BaseResponse.internal(message=str(e))
