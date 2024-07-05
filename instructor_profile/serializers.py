from rest_framework import serializers

from instructor_profile.models import InstructorProfile


class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        read_only_fields = ("id",)
        fields = "__all__"


class InstructorProfileViewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = InstructorProfile
        exclude = ["user"]
