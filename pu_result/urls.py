from django.urls import path

from .views import ResultQueryView, ResultView

urlpatterns = [
    path("", ResultView.as_view(), name="results"),
    path("result/<symbol_number>/", ResultQueryView.as_view(), name="result-symbol")
]
