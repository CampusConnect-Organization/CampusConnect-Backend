from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


ATTENDANCE_STATUS = (
    ("absent", "Absent"),
    ("present", "Present"),
)


class Attendance(models.Model):
    course_session = models.ForeignKey(
        "courses.CourseSession", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        "student_profile.StudentProfile", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            today = date.today()
            existing_attendance = Attendance.objects.filter(
                course_session=self.course_session,
                student=self.student,
                date__date=today,
            ).exists()

            if existing_attendance:
                raise ValidationError("Attendance has already been taken today.")

        super().save(*args, **kwargs)
