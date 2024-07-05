from django.urls import path

from .views.student_profile import StudentProfileView

urlpatterns = [
    path("", StudentProfileView.as_view(), name="student-profile"),
]
