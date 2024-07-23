from django.urls import path

from attendance.views import (
    AttendanceListView,
    MarkAttendanceAbsentView,
    MarkAttendancePresentView,
    StudentAttendanceListView,
    VideoFeedView,
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
    path("attendance_video/", VideoFeedView.as_view(), name="attendance-video"),
]
