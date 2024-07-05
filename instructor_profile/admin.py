from django.contrib import admin
from django.contrib import messages

from instructor_profile.models import InstructorProfile
from student_profile.models import StudentProfile


# Register your models here.
@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone_number",
        "gender",
        "faculty",
        "address",
        "education",
    )
    search_fields = ("user__username", "user__email")

    def save_model(self, request, obj, form, change):
        if StudentProfile.objects.filter(user=obj.user).exists():
            messages.error(request, "A student profile already exists for this user.")
            return
        super().save_model(request, obj, form, change)
