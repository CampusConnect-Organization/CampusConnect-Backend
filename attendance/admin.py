from django.contrib import admin

from attendance.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "course_session", "student", "status", "date"]
    list_filter = ["course_session", "student", "status", "date"]
    search_fields = ["course_session__name", "student__name"]
    readonly_fields = ["date"]

    def has_add_permission(self, request):
        # Prevent adding new attendance records
        return True

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting attendance records
        return False

    def has_change_permission(self, request, obj=None):
        # Allow changing attendance records
        return True
