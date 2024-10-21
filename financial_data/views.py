import json
import logging
from typing import Dict

from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from financial_data.tasks import add_symbol, get_data, get_symbols, periodic_update

logger = logging.getLogger("financial_data")
logger.setLevel(logging.CRITICAL)


def stock_analyzer_view(request: HttpRequest) -> HttpResponse:
    """
    The default stock_analyzer_view
    """
    logger.info(request)
    if request.method == "POST":
        if "add_symbol" in request.POST:
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

        elif "refresh_existing" in request.POST:
            periodic_update()

    return render(request, "stock_analyzer.html")


def view_data(request: HttpRequest) -> HttpResponse:
    """
    Endpoint to view all the data
    """
    symbol = request.GET.get("symbol", None)
    json_resp: Dict = {"status": "OK"}

    if symbol is None:
        json_resp["data"] = get_symbols()
        json_data = json.dumps(json_resp)
        return HttpResponse(json_data, content_type="application/json")

    json_resp["data"] = get_data(symbol)
    json_resp["symbol"] = symbol
    json_data = json.dumps(json_resp)
    return HttpResponse(json_data, content_type="application/json")
