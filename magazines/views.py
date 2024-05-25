from django.http import HttpRequest
from django.shortcuts import render, reverse, redirect


def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            "title": "Home"
        }
    )


def magazines(request):
    pass
