from rest_framework.views import APIView
from rest_framework import status
from app.services.accountsService import AccountsService
from app.mapping.accountsMapping import AccountsMapping
from app.utils.baseResponse import BaseResponse
from app.utils.dictHelper import DictHelper
import logging

log = logging.getLogger(__name__)

class AccountsController(APIView):

    def post(self, request, action = None):
        try:
            if action and action == "user/search":
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
                return BaseResponse.error(message="Thông tin tìm kiếm không hợp lệ")
            
            if action == "login":                
                username = str(request.data.get("username"))
                email = str(request.data.get("email"))
                password = str(request.data.get("password"))
                if (username or email) and password:
                    result = AccountsService.login(request.data)
                    if result:
                        account = result.get("account")
                        if account:
                            if not account.is_active:
                                result["account"] = "account_deactivated"
                            else:
                                result["account"] = AccountsMapping(account).data
                            return BaseResponse.success(data=result)
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Sai tài khoản hoặc mật khẩu")
                return BaseResponse.error(message= "Thiếu thông tin đăng nhập")
            
            if action == "validate-token":
                account_id = str(request.user_id)
                if account_id:
                    result = AccountsService.validate_token(account_id=account_id)
                    if result:
                        account = result.get("account")
                        if account:
                            if not account.is_active:
                                result["account"] = "deactivated"
                            else:
                                result["account"] = AccountsMapping(account).data
                            return BaseResponse.success(data=result)
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "token không hợp lệ")
                return BaseResponse.error(message="Thiếu token")
            
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
                    return BaseResponse.custom(status.HTTP_401_UNAUTHORIZED, "Đăng ký thất bại")
                return BaseResponse.error(message= "Thiếu thông tin đăng ký")
            
            if action and action == "restock-token":
                token = request.data.get("token")
                if token:
                    result = AccountsService.restock_token(token)
                    if result:
                        return BaseResponse.success(data=result)
                    return BaseResponse.custom(status_code=status.HTTP_401_UNAUTHORIZED, message="Token không hợp lệ")
                return BaseResponse.error(message="Thiếu token")
            
            if action and action == "user/all-users":
                data = request.data or {}
                result = AccountsService.find_all_paginated(data)
                if result:
                    result["page_content"] = AccountsMapping(result.get("page_content", []), many=True).data
                    return BaseResponse.success(data=result)
                return BaseResponse.error(message="Dữ liệu không hợp lệ")
            
            return BaseResponse.internal(message=str(e))
        except Exception as e:
            return BaseResponse.internal(message=str(e))