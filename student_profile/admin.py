from django.contrib import admin

from instructor_profile.models import InstructorProfile
from .models import StudentProfile
from django.contrib import messages
from courses.models import Course, CourseEnrollment, StudentCourse


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "gender",
        "date_of_birth",
        "address",
        "academics",
        "is_verified",
    )
    list_filter = ("is_verified",)
    search_fields = (
        "user__username",
        "user__email",
        "first_name",
        "last_name",
        "phone",
        "address",
        "academics",
    )

    def save_model(self, request, obj, form, change):
        if InstructorProfile.objects.filter(user=obj.user).exists():
            messages.error(
                request, "An instructor profile already exists for this user."
            )
            return

        if change and "semester" in form.changed_data:
            StudentCourse.objects.filter(student=obj).delete()

        super().save_model(request, obj, form, change)

        if "semester" in form.changed_data:
            semester = obj.semester

            courses = Course.objects.filter(semester=semester)

            for course in courses:
                StudentCourse.objects.get_or_create(student=obj, course=course)


admin.site.register(StudentProfile, StudentProfileAdmin)
