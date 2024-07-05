from rest_framework import serializers

from grades.models import Exam, GradeRecord


class ExamSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(
        source="course_session.instructor.full_name"
    )
    course_session_name = serializers.CharField(source="course_session.course.title")
    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.time.strftime("%I:%M %p")

    class Meta:
        model = Exam
        fields = "__all__"


class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


class GradeRecordSerializer(serializers.ModelSerializer):
    exam = serializers.CharField(source="exam.course_session.course.title")
    full_marks = serializers.IntegerField(source="exam.total_marks")
    has_passed = serializers.BooleanField()
    instructor_name = serializers.CharField(
        source="exam.course_session.instructor.full_name"
    )

    class Meta:
        model = GradeRecord
        fields = "__all__"
