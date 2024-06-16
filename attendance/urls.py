from django.urls import path

from attendance.views import (
    AttendanceListView,
    MarkAttendanceAbsentView,
    MarkAttendancePresentView,
    StudentAttendanceListView,
)

urlpatterns = [
    path("attendances/<int:pk>/", AttendanceListView.as_view(), name="attendances"),
    path("mark-present/", MarkAttendancePresentView.as_view(), name="mark-present"),
    path("mark-absent/", MarkAttendanceAbsentView.as_view(), name="mark-absent"),
    path(
        "list-attendances/<int:pk>/",
        StudentAttendanceListView.as_view(),
        name="student-attendance",
    ),
]
