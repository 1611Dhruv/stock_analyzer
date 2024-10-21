import os

from django.http import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from ai_integration.predictor import (
    SymbolDNE,
    generate_pdf_predictions,
    predict_and_save,
)

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

    # Return a PDF output if requested
    if "format" in request.GET and request.GET["format"] == "pdf":
        path = generate_pdf_predictions(prediction_df)
        with open(path, "rb") as file:
            response = HttpResponse(file.read(), content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="prediction_report.pdf"'
            os.remove(path)
            return response

    response = {"status": "OK", "data": prediction_df.to_dict()}
    return JsonResponse(response)
