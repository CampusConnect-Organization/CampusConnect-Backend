from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.response import CustomResponse


def handle_other_exceptions(exc, context):
    # For all other exceptions that DRF does not handle.
    headers = {}
    data = {"detail": str(exc)}
    return Response(data, status=500, headers=headers)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        response = handle_other_exceptions(exc, context)

    return CustomResponse.error(
        message=response.status_text,
        data=response.data,
        status_code=response.status_code,
    )
