import logging
from typing import Dict

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http.response import HttpResponseBadRequest

from financial_data.tasks import add_symbol, get_data, get_symbols, periodic_update

logger = logging.getLogger("financial_data")
logger.setLevel(logging.CRITICAL)


def add_symbol_view(request: HttpRequest) -> HttpResponse:
    """
    The post request endpoint which adds a symbol to the database
    """
    if request.method == "POST":
        if "symbol" in request.POST:
            # Try getting the symbol object from the POST request
            symbol = request.POST.get("symbol")
            if symbol is None:
                logger.error("The post request recieved had no symbol field")
                return HttpResponseBadRequest("stock symbol is missing")

            try:
                add_symbol(symbol)
            except Exception as e:
                logger.error(e)
                return HttpResponseBadRequest(e)

    return HttpResponseBadRequest("Invalid request")


def refresh_symbols_view(request: HttpRequest) -> HttpResponse:
    """
    The post request endpoint which adds a symbol to the database
    """
    if request.method == "POST":
        periodic_update()
    return HttpResponseBadRequest("Invalid request")


def list_data_view(request: HttpRequest) -> HttpResponse:
    """
    Endpoint to view all the existing stock data in the database
    """
    symbol = request.GET.get("symbol", None)
    json_resp: Dict = {"status": "OK"}

    if symbol is None:
        json_resp["data"] = get_symbols()
        return JsonResponse(json_resp)

    json_resp["data"] = get_data(symbol)
    json_resp["symbol"] = symbol
    return JsonResponse(json_resp)
