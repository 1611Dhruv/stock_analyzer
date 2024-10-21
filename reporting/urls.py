from django.urls import path

from financial_data.views import stock_analyzer_view, view_data

urlpatterns = [
    path("", stock_analyzer_view, name="stock_analyzer_view"),
    path("data", view_data, name="view_data"),
]
