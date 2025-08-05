from rest_framework.views import APIView
from app.utils.baseResponse import BaseResponse
from app.services.mediasService import MediasService
import json

class MediasController(APIView):
    def post(self, request, action):
        try:
            if action and action == "upload":
                file = request.FILES.get('file')
                metadata_from_request = request.data.get("metadata")

                if not file:
                    return BaseResponse.error("Không tìm thấy file")
                
                try:
                    metadata = json.loads(metadata_from_request) if metadata_from_request else {}
                except Exception as e:
                    return BaseResponse.error("Metadata không phải JSON hợp lệ")

                result = MediasService.storage_media_file(file, metadata)
                if result:
                    return BaseResponse.success(data=result)
                return BaseResponse.error("upload thất bại")
            return BaseResponse.internal()
        except Exception as e:
            return BaseResponse.internal(message=str(e))