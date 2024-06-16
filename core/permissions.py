from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    DjangoModelPermissions,
)
from rest_framework.request import Request


class CustomPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class IsAuthenticatedAndReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )


class IsInstructor(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user.is_authenticated and request.user.instructorprofile)


class IsStudent(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user.is_authenticated and request.user.studentprofile)
