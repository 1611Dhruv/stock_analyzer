from django.urls import path

from financial_data.views import add_symbol_view, list_data_view, refresh_symbols_view

urlpatterns = [
    path("add/", add_symbol_view),
    path("refresh/", refresh_symbols_view),
    path("data/", list_data_view, name="list_data_view"),
]
