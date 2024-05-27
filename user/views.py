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


def signup(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'signup.html',
        {
            "title": "Sign Up"
        }
    )


def logout(request):
    pass