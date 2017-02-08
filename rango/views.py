from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Rango says hey there partner!')

def test(request):
    pass