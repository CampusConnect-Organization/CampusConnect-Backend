# type: ignore
from django.contrib import admin

from student_profile.models import StudentProfile
from django.contrib import messages
from .models import (
    Course,
    CourseSession,
    CourseEnrollment,
    StudentCourse,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "course_code", "semester")
    search_fields = ("title", "course_code", "description", "semester")


@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ("course", "start", "end", "instructor")
    list_filter = ("course",)
    search_fields = ("course__title", "instructor__user__username")


@admin.register(StudentCourse)
class StudentCoursesAdmin(admin.ModelAdmin):
    list_display = ("student", "course")
    search_fields = (
        "student__user__username",
        "student__user__email",
        "course__title",
    )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course_session")
    search_fields = (
        "student__user__username",
        "student__user__email",
        "course_session__course__title",
    )
