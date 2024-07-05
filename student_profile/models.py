from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Course, CourseEnrollment, StudentCourse


User = get_user_model()

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)

SEMESTER_CHOICES = (
    ("1st", "1st"),
    ("2nd", "2nd"),
    ("3rd", "3rd"),
    ("4th", "4th"),
    ("5th", "5th"),
    ("6th", "6th"),
    ("7th", "7th"),
    ("8th", "8th"),
)


class StudentProfile(models.Model):
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="avatars/students/"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)
    academics = models.TextField()
    is_verified = models.BooleanField(default=False)
    symbol_number = models.CharField(null=True, max_length=50, blank=True)
    semester = models.CharField(choices=SEMESTER_CHOICES, max_length=50)

    def __str__(self) -> str:  # type: ignore
        return f"{self.full_name}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.type = "student"  # type: ignore
        self.user.save()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


@receiver(post_save, sender=StudentProfile)
def enroll_student_in_courses(sender, instance, created, **kwargs):
    if created or not instance.pk:
        semester = instance.semester
    else:
        old_instance = StudentProfile.objects.get(pk=instance.pk)
        if instance.semester != old_instance.semester:
            semester = instance.semester
        else:
            return

        StudentCourse.objects.filter(student=instance).delete()

    courses = Course.objects.filter(semester=semester)

    for course in courses:
        StudentCourse.objects.get_or_create(student=instance, course=course)
