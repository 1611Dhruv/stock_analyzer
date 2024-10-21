from django.shortcuts import render

# Create your views here.


def reporting_view(request):
    return render(request, "reporting.html")
