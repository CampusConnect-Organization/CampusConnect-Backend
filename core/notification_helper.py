from firebase_admin.messaging import Notification, Message
from fcm_django.models import FCMDevice
from notification.models import Notification as NotificationModel


def send_notification(title, body):
    devices = FCMDevice.objects.all()
    # NotificationModel.objects.create(title=title, body=body)
    for device in devices:
        device.send_message(
            Message(
                notification=Notification(
                    title=title,
                    body=body,
                )
            )
        )
