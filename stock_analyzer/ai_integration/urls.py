from ai_integration.views import ai_prediction_view
from django.urls import path

urlpatterns = [
    path("", ai_prediction_view, name="ai predictions"),
]
