from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from fcm_django.models import FCMDevice
from core.response import CustomResponse
from firebase_admin.messaging import Notification, Message


from notification.models import NotificationDevice
from notification.models import Notification as NotificationModel
from notification.serializers import NotificationSerializer


# Create your views here.
class RegisterFCMDevice(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        device = FCMDevice(registration_id=request.data.get("device_id"))  # type: ignore
        device.save()

        NotificationDevice.objects.create(user=request.user, device=device)

        return CustomResponse.success(message="Device registered for FCM successfully!")


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request: Request):
        notifications = NotificationModel.objects.all()
        serializer = self.serializer_class(instance=notifications, many=True)

        return CustomResponse.success(
            serializer.data, message="Notifications fetched successfully!"
        )


class SendNotification(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def post(self, request: Request):
        devices = FCMDevice.objects.all()
        serializer = self.serializer_class(data=request.data)  # type: ignore
        if serializer.is_valid():
            # NotificationModel.objects.create(
            #     title=serializer.data.get("title"),
            #     body=serializer.data.get("body"),
            # )
            for device in devices:
                device.send_message(
                    Message(
                        notification=Notification(
                            title=serializer.data.get("title"),
                            body=serializer.data.get("body"),
                        )
                    )
                )

            return CustomResponse.success(
                message="Notifications sent out!", data=serializer.data
            )
