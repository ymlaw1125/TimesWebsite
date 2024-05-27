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


def login(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'login.html',
        {
            "title": "Log In"
        }
    )


def logout(request):
    pass