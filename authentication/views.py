# type: ignore
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request

from authentication.models import BlacklistedToken
from authentication.serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
)
from core.response import CustomResponse

from .authentication import JWTAuthentication as jwt_auth

User = get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            access_token, refresh_token = jwt_auth.create_tokens(user)
            return CustomResponse.success(
                data={"access_token": access_token, "refresh_token": refresh_token},
                message="User registered successfully!",
            )
        return CustomResponse.error(message="User already exists!")


class RefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = jwt_auth.refresh_access_token(
            serializer.validated_data.get("refresh_token")
        )

        return CustomResponse.success(
            data={"access_token": access_token},
            message="Access token refreshed successfully!",
        )


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return CustomResponse.error(message="Invalid credentials provided")

        if not user.type in ["user", "student"]:
            return CustomResponse.error(
                message="Only students are allowed to login!",
                status_code=401,
            )

        access_token, refresh_token = jwt_auth.create_tokens(user)

        return CustomResponse.success(
            data={"access_token": access_token, "refresh_token": refresh_token},
            message="User logged in successfully!",
        )


class InstructorLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return CustomResponse.error(message="Invalid credentials provided")

        if not user.type == "instructor":
            return CustomResponse.error(
                message="Only instructors are allowed to login!",
                status_code=401,
            )

        access_token, refresh_token = jwt_auth.create_tokens(user)

        return CustomResponse.success(
            data={"access_token": access_token, "refresh_token": refresh_token},
            message="User logged in successfully!",
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        BlacklistedToken.objects.create(token=request.auth)
        return CustomResponse.success(message="User logged out successfully!")
