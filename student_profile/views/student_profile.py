import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from student_profile.models import StudentProfile
from student_profile.serializers import (
    StudentProfileCreateSerializer,
    StudentProfileViewSerializer,
)
from rest_framework.request import Request

from core.response import CustomResponse

User = get_user_model()


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileCreateSerializer
    view_serializer_class = StudentProfileViewSerializer

    def get(self, request: Request):
        student_profile = StudentProfile.objects.filter(user=request.user).first()

        if not student_profile:
            return CustomResponse.error(
                message="Student profile doesn't exist!",
                status_code=404,
            )
        serializer = self.view_serializer_class(instance=student_profile)
        return CustomResponse.success(
            data=serializer.data,
            message="Profile fetched successfully!",
        )

    def post(self, request: Request):
        user_dict = {"user": request.user.id}
        data = {
            **request.data,  # type: ignore
            **user_dict,
        }
        merged_data = {}
        merged_data.update(json.loads(data["data"][0]))
        merged_data["profile_picture"] = data["profile_picture"][0]
        merged_data["user"] = data["user"]
        serializer = self.serializer_class(data=merged_data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            data=serializer.data, message="Profile created successfully!"
        )
