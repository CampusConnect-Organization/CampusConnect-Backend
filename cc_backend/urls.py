"""
URL configuration for cc_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/student-profile/", include("student_profile.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/grades/", include("grades.urls")),
    path("api/library/", include("library.urls")),
    path("api/results/", include("pu_result.urls")),
    path("api/notification/", include("notification.urls")),
    path("api/instructor/", include("instructor_profile.urls")),
    path("api/attendance/", include("attendance.urls")),
    re_path(r"^plate/", include("django_spaghetti.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
