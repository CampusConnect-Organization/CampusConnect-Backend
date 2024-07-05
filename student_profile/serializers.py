from rest_framework import serializers

from student_profile.models import StudentProfile


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        read_only_fields = ("id",)
        fields = "__all__"


class StudentProfileViewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = StudentProfile
        exclude = ["user"]
