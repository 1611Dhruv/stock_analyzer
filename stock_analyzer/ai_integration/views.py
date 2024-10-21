from ai_integration.predictor import SymbolDNE, predict_and_save
from django.http import HttpRequest
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.


def ai_prediction_view(request: HttpRequest):
    """
    Get the ai's prediction for the given stock
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Request was not a get request")

    symbol = request.GET.get("symbol")
    if symbol is None:
        return HttpResponseBadRequest("Request did not have a symbol param")

    # Otherwise get the predictions for this symbol
    try:
        prediction_df = predict_and_save(symbol)
    except SymbolDNE:
        return HttpResponseBadRequest("The symbol was a bad param")

    response = {"status": "OK", "data": prediction_df.to_dict()}
    return JsonResponse(response)
