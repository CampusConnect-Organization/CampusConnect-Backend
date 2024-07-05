from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


FACULTY_CHOICES = (
    ("civil", "Civil"),
    ("computer", "Computer"),
    ("architecture", "Architecture"),
)

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)


# Create your models here.
class InstructorProfile(models.Model):
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="avatars/instructors/"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    faculty = models.CharField(max_length=30, choices=FACULTY_CHOICES)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    education = models.TextField()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.type = "instructor"  # type: ignore
        self.user.save()

    def __str__(self):
        return self.full_name
