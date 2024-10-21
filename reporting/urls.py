from django.urls import path

from reporting.views import reporting_view

urlpatterns = [
    path("", reporting_view, name="reporting_view"),
]
