from django.urls import path

from backtesting.views import backtesting_view

urlpatterns = [
    path("", backtesting_view, name="backtesting"),
]
