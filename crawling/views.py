#views.py
from django.http import HttpResponse


def crawling(request, string):
    return HttpResponse("Hello, world. Crawling Test." + "number = " + string)