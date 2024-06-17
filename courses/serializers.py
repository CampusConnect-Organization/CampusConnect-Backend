from rest_framework import serializers

from courses.models import Course, CourseEnrollment, CourseSession, StudentCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseSessionSerializer(serializers.ModelSerializer):
    course = serializers.CharField()
    instructor = serializers.CharField()

    class Meta:
        model = CourseSession
        fields = "__all__"


class StudentCoursesSerializer(serializers.ModelSerializer):
    course = serializers.CharField()
    semester = serializers.CharField(source="course.semester")
    course_code = serializers.CharField(source="course.course_code")

    class Meta:
        model = StudentCourse
        fields = ["id", "course", "semester", "course_code"]


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(
        source="course_session.instructor.full_name"
    )

    course_session_name = serializers.CharField(source="course_session.course.title")
    course_session_id = serializers.IntegerField(source="course_session.id")
    start_date = serializers.DateField(source="course_session.start")
    end_date = serializers.DateField(source="course_session.end")
    semester = serializers.CharField(source="course_session.course.semester")

    class Meta:
        model = CourseEnrollment
        fields = [
            "id",
            "instructor_name",
            "course_session_name",
            "course_session_id",
            "start_date",
            "end_date",
            "semester",
        ]


class CourseEnrollmentStudentsSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name")
    course_session_name = serializers.CharField(source="course_session.course.title")
    course_session_id = serializers.IntegerField(source="course_session.id")

    class Meta:
        model = CourseEnrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course_session_name",
            "course_session_id",
        ]


class CourseEnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = "__all__"
