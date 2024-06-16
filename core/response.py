from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    @staticmethod
    def success(data=None, message="", status_code=status.HTTP_200_OK):
        return Response(
            data={"success": True, "data": data, "message": message},
            status=status_code,
        )

    @staticmethod
    def error(message="", data=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            data={"success": False, "errors": data, "message": message},
            status=status_code,
        )
