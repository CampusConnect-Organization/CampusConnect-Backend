from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from core.response import CustomResponse
from pu_result.models import Result
from pu_result.serializers import ResultSerializer


class ResultView(APIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        if request.user.type != "student":
            return CustomResponse.error(
                "Only students can access this route", status_code=401
            )
        if not request.user.studentprofile.symbol_number:
            return CustomResponse.error("Cannot access route, symbol number not set!")
        results = Result.objects.filter(
            symbol_number=request.user.studentprofile.symbol_number
        )
        if len(results) == 0:
            return CustomResponse.error("Results not found!")

        serializer = self.serializer_class(results, many=True)

        return CustomResponse.success(
            data=serializer.data,
            message="Result fetched successfully!",
        )


class ResultQueryView(APIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, symbol_number: str):
        results = Result.objects.filter(symbol_number=symbol_number)
        if len(results) == 0:
            return CustomResponse.error("Results not found!")

        serializer = self.serializer_class(results, many=True)

        return CustomResponse.success(
            data=serializer.data,
            message=f"Result of {symbol_number} fetched successfully!",
        )
