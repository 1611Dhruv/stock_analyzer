import os

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from backtesting.tasks import generate_json_backtest, generate_pdf_backtest

# Create your views here.


def backtesting_view(request):
    if request.method == "GET":
        if (
            "symbol" not in request.GET
            or "amt" not in request.GET
            or "winbuy" not in request.GET
            or "winsell" not in request.GET
        ):
            return HttpResponseBadRequest("Missing required parameters")

        symbol = request.GET.get("symbol")
        try:
            amt = float(request.GET.get("amt"))
            winbuy = int(request.GET.get("winbuy"))
            winsell = int(request.GET.get("winsell"))
        except ValueError:
            return HttpResponseBadRequest("The value supplied was not appropriate")

        format = request.GET.get("format")
        if format is None:
            format = "json"

        if format == "pdf":
            path = generate_pdf_backtest(symbol, amt, winbuy, winsell)
            with open(path, "rb") as file:
                response = HttpResponse(file.read(), content_type="application/pdf")
                response["Content-Disposition"] = (
                    'inline; filename="backtesting_report.pdf"'
                )
                os.remove(path)
                return response
        if format != "json":
            return HttpResponseBadRequest("Unknowown format")

        json = generate_json_backtest(symbol, amt, winbuy, winsell)
        return JsonResponse({"status": "OK", "data": json})

    return HttpResponseBadRequest("Invalid request")
