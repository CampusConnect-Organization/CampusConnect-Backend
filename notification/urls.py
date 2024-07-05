from django.urls import path

from notification.views import NotificationView, RegisterFCMDevice, SendNotification


urlpatterns = [
    path("register-fcm/", RegisterFCMDevice.as_view(), name="register-fcm"),
    path("send-notification/", SendNotification.as_view(), name="send-notification"),
    path("", NotificationView.as_view(), name="notifications"),
]
