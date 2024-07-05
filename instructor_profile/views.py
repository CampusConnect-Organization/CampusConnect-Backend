import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from instructor_profile.models import InstructorProfile
from instructor_profile.serializers import (
    InstructorProfileSerializer,
    InstructorProfileViewSerializer,
)
from student_profile.serializers import StudentProfileViewSerializer
from student_profile.models import StudentProfile
from rest_framework.request import Request
from core.response import CustomResponse
from core.permissions import IsInstructor

User = get_user_model()


class InstructorProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstructorProfileSerializer
    view_serializer_class = InstructorProfileViewSerializer

    def get(self, request: Request):
        instructor_profile = InstructorProfile.objects.filter(user=request.user).first()

        if not instructor_profile:
            return CustomResponse.error(
                message="Instructor profile doesn't exist!", status_code=404
            )
        serializer = self.view_serializer_class(instance=instructor_profile)
        return CustomResponse.success(
            data=serializer.data,
            message="Instructor profile fetched successfully!",
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
            data=serializer.data, message="Instructor profile created successfully!"
        )


class StudentListView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = StudentProfileViewSerializer

    def get(self, request: Request):
        students = StudentProfile.objects.all()

        serializer = self.serializer_class(instance=students, many=True)

        return CustomResponse.success(
            data=serializer.data,
            message="Students fetched successfully!",
        )
