from datetime import date

import cv2
import numpy as np
import face_recognition

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from attendance.models import Attendance
from core.permissions import IsInstructor, IsStudent
from core.response import CustomResponse
from student_profile.models import StudentProfile
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


class VideoFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        file_obj = request.data.get("file")
        course_session = request.data.get("course_session")
        bytes_data = file_obj.read()
        nparr = np.frombuffer(bytes_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for face_encoding in face_encodings:
            student = self.compare_faces(face_encoding)
            if student:
                if student.user.id != request.user.id:
                    return CustomResponse.error(
                        message="You are not allowed to mark attendance for other students!"
                    )
                self.update_attendance(student, course_session)
            else:
                return CustomResponse.error(
                    message="No student found!", status_code=418
                )

        return CustomResponse.success(message="Attendance marked successfully!")

    def compare_faces(self, face_encoding):
        students = StudentProfile.objects.exclude(face_encoding=None)
        for student in students:
            known_encoding = student.get_face_encoding()
            results = face_recognition.compare_faces([known_encoding], face_encoding)
            if results[0]:
                return student
        return None

    def update_attendance(self, student, course_session):
        today = date.today()

        attendance, created = Attendance.objects.get_or_create(
            course_session_id=course_session,
            student=student,
            date__date=today,
            defaults={"status": "present"},
        )

        if not created:
            attendance.status = "present"
            attendance.save()
