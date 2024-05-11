from django.http import HttpRequest
from django.shortcuts import render, reverse, redirect

# Create your views here.
def library(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'user_lib.html',
        {
            "title": "Library"
        }
    )