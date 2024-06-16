from django.contrib.auth.models import AbstractUser
from django.db import models

USER_TYPE_CHOICES = (
    ("admin", "Administrator"),
    ("registrar", "Registrar"),
    ("instructor", "Instructor"),
    ("student", "Student"),
    ("user", "User"),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="user",
    )


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
