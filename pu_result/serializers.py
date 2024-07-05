from rest_framework import serializers

from pu_result.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"