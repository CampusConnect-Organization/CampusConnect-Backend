# type: ignore
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from core.response import CustomResponse
from core.permissions import IsInstructor
from courses.models import CourseEnrollment
from grades.models import Exam, GradeRecord
from django.utils import timezone

from grades.serializers import (
    GradeRecordSerializer,
    ExamSerializer,
    ExamCreateSerializer,
)


class ExamView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = ExamCreateSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return CustomResponse.success(
            data=serializer.data,
            message="Exam created successfully!",
        )


class ExamListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExamSerializer

    def get(self, request):
        course_enrollments = CourseEnrollment.objects.filter(
            student=request.user.studentprofile
        )

        exams = Exam.objects.filter(
            course_session__in=course_enrollments.values("course_session"),
            date__gte=timezone.now().date(),
        ).order_by("date")

        serializer = self.serializer_class(instance=exams, many=True)

        return CustomResponse.success(
            data=serializer.data, message="Upcoming exams fetched successfully!"
        )


class GradeListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeRecordSerializer

    def get(self, request):
        grades = GradeRecord.objects.filter(student__user=request.user).all()
        serializer = self.serializer_class(instance=grades, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Grades fetched successfully!"
        )


class GradeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeRecordSerializer

    def get(self, request, pk: int):
        grade = GradeRecord.objects.filter(student__user=request.user, id=pk).first()
        if not grade:
            return CustomResponse.error(
                message=f"Grade record with ID {pk} doesn't exist!", status_code=404
            )
        serializer = self.serializer_class(instance=grade)

        return CustomResponse.success(
            data=serializer.data,
            message="Grade record fetched successfully!",
        )
