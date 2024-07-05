from django.db import models
from fcm_django.models import FCMDevice


class NotificationDevice(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    device = models.ForeignKey(FCMDevice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}{self.device}"


class Notification(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"
