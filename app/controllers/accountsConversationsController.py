from rest_framework.views import APIView
from app.utils.baseResponse import BaseResponse
from app.services.accountsConversationsService import AccountsConversationsService
from app.mapping.conversationsMapping import ConversationsMapping


class AccountsConversationsController(APIView):
    def post(self, request, action):
        try:
            if action and action == "load-account-conversations":
                data = request.data
                data["account_id"] = str(request.user_id)
                response = AccountsConversationsService.find_by_account_paginated(data=data)
                list_ac = response["page_content"]
                result = [ac.get_conversation for ac in list_ac]
                response["page_content"] = ConversationsMapping(result, many=True).data
                return BaseResponse.success(data=response)
            return BaseResponse.error()
        except Exception:
            return BaseResponse.internal(message=f"lỗi ở đây {str(e)}")