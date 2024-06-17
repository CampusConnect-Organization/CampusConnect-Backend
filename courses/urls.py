from django.urls import path

import courses.views as courseView


urlpatterns = [
    path("courses/", courseView.CourseListView.as_view(), name="courses"),
    path("course/<pk>/", courseView.CourseDetailView.as_view(), name="course"),
    path(
        "semester/<semester>/",
        courseView.CourseSemesterView.as_view(),
        name="course-semester",
    ),
    path("sessions/", courseView.CourseSessionListView.as_view(), name="sessions"),
    path("session/<pk>/", courseView.CourseSessionDetailView.as_view(), name="session"),
    path(
        "student-courses/",
        courseView.StudentCoursesListView.as_view(),
        name="student-courses",
    ),
    path(
        "student-course/<pk>/",
        courseView.StudentCourseDetailView.as_view(),
        name="student-course",
    ),
    path(
        "enrollments/",
        courseView.CourseEnrollmentListView.as_view(),
        name="enrollments",
    ),
    path(
        "enrollment/<pk>/",
        courseView.CourseEnrollmentDetailView.as_view(),
        name="enrollment",
    ),
    path(
        "create-enrollment/",
        courseView.CourseEnrollmentCreateView.as_view(),
        name="create-enrollment",
    ),
]

urlpatterns += [
    path(
        "instructor-courses/",
        courseView.CourseSessionInstructorView.as_view(),
        name="instructor-courses",
    ),
    path(
        "instructor-courses/enrolls/<int:pk>/",
        courseView.EnrolledStudentsView.as_view(),
        name="enrolled-students",
    ),
]
