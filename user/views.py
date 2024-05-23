from django.http import HttpRequest
from django.shortcuts import render, reverse, redirect


def library(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'user_lib.html',
        {
            "title": "Library"
        }
    )

def click_magazines(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'click_magazine.html',
        {
            "title": "Magazine"
        }
    )

def login(request):
    pass


def logout(request):
    pass