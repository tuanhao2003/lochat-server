from rest_framework.response import Response
from rest_framework import status


class BaseResponse:
    @staticmethod
    def success(status_code=status.HTTP_200_OK, message="Success", data=None):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")

    @staticmethod
    def error(status_code=status.HTTP_400_BAD_REQUEST, message="Something went wrong", data=None):
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
    
    @staticmethod
    def not_found(status_code=status.HTTP_404_NOT_FOUND, message="Not found", data=None):
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
    
    @staticmethod
    def internal(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal server error", data=None):
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
    
    @staticmethod
    def custom(status_code: status, message: str, data=None):
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=status_code, content_type="application/json; charset=utf-8")
