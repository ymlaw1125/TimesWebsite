from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest
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


def magazine(request, magazine_id):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'magazine.html',
        {
            "title": "Magazine",
            "id": magazine_id,
        }
    )


def library(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'library.html',
        {
            "title": "Library"
        }
    )
