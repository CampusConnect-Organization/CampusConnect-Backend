from django.db import models
from courses.models import CourseSession
from student_profile.models import StudentProfile

EXAM_TYPE_CHOICES = (
    ("internal", "Internal"),
    ("final", "Final"),
    ("practical", "Practical"),
)


class Exam(models.Model):
    course_session = models.ForeignKey(CourseSession, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    total_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=45)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.course_session.course.title}'s {self.exam_type} exam"


class GradeRecord(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    class Meta:
        unique_together = ("exam", "student")

    @property
    def has_passed(self):
        return True if self.marks_obtained >= self.exam.pass_marks else False
