from django.urls import path

from grades.views import ExamView, GradeDetailView, GradeListView, ExamListView


urlpatterns = [
    path("all/", GradeListView.as_view(), name="grade-list"),
    path("grade/<pk>/", GradeDetailView.as_view(), name="grade-detail"),
    path("exams/", ExamListView.as_view(), name="exams"),
    path("exam/", ExamView.as_view(), name="exam"),
]
