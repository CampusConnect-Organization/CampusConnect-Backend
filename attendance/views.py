from datetime import date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from attendance.models import Attendance
from core.permissions import IsInstructor, IsStudent
from core.response import CustomResponse
from .serializers import AttendanceSerializer, AttendanceViewSerializer
from rest_framework.request import Request


class AttendanceListView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = AttendanceViewSerializer

    def get(self, request: Request, pk: int):
        attendances = Attendance.objects.filter(
            course_session__instructor=request.user.instructorprofile,
            course_session=pk,
        ).all()
        serializer = self.serializer_class(instance=attendances, many=True)

        return CustomResponse.success(
            data=serializer.data,
            message="Attendances fetched successfully!",
        )


class MarkAttendancePresentView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = AttendanceSerializer

    def post(self, request: Request):
        today = date.today()

        attendance = Attendance.objects.filter(
            course_session=request.data.get("course_session"),  # type: ignore
            student=request.data.get("student"),  # type: ignore
            date__date=today,
        ).first()

        if attendance:
            attendance.status = "present"
            attendance.save()
        else:
            updated_data = {
                "status": "present",
                **request.data,  # type: ignore
            }
            serializer = self.serializer_class(data=updated_data)  # type: ignore
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return CustomResponse.success(message="Attendance marked as present!")


class MarkAttendanceAbsentView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = AttendanceSerializer

    def post(self, request: Request):
        today = date.today()

        attendance = Attendance.objects.filter(
            course_session=request.data.get("course_session"),  # type: ignore
            student=request.data.get("student"),  # type: ignore
            date__date=today,
        ).first()

        if attendance:
            attendance.status = "absent"
            attendance.save()
        else:
            updated_data = {
                "status": "absent",
                **request.data,  # type: ignore
            }
            serializer = self.serializer_class(data=updated_data)  # type: ignore
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return CustomResponse.success(message="Attendance marked as absent!")


class StudentAttendanceListView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = AttendanceViewSerializer

    def get(self, request: Request, pk: int):
        attendances = Attendance.objects.filter(
            course_session=pk,
            student=request.user.studentprofile,
        ).all()

        serializer = self.serializer_class(instance=attendances, many=True)

        return CustomResponse.success(
            data=serializer.data,
            message="Attendances fetched successfully!",
        )
