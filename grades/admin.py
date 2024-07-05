# type: ignore
from django import forms
from django.contrib import admin
from core.notification_helper import send_notification
from courses.models import CourseEnrollment

from student_profile.models import StudentProfile
from .models import Exam, GradeRecord


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("course_session", "exam_type", "total_marks", "date")
    list_filter = ("course_session", "exam_type", "date")
    search_fields = ("course_session__course__title", "exam_type", "date")

    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)

            title = "New Exam Created"
            body = f"Subject: {obj.course_session.course.title}\nExam Type: {obj.exam_type.title()}\nTotal Marks: {obj.total_marks}\nDate: {obj.date}\nTime: {obj.time}"

            send_notification(title, body)
        else:
            super().save_model(request, obj, form, change)


@admin.register(GradeRecord)
class GradeRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "exam", "marks_obtained")
    list_filter = (
        "exam__course_session__course__title",
        "exam__exam_type",
    )
    search_fields = ("student__user__email", "exam__course_session__course__title")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            student_profiles = StudentProfile.objects.all()
            course_enrollments = CourseEnrollment.objects.filter(
                student__in=student_profiles
            )
            kwargs["queryset"] = student_profiles.filter(
                courseenrollment__in=course_enrollments
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def clean(self):
        cleaned_data = super().clean()  # type: ignore
        student = cleaned_data.get("student")
        if not CourseEnrollment.objects.filter(student=student).exists():
            raise forms.ValidationError("Student is not enrolled in any course.")
        return cleaned_data
