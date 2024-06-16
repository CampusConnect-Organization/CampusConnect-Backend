from rest_framework import serializers

from attendance.models import Attendance


class AttendanceViewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name")
    course_session = serializers.CharField()

    class Meta:
        model = Attendance
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
