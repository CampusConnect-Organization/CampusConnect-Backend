from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
