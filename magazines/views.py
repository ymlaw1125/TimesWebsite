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


def click_magazines(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'click_magazine.html',
        {
            "title": "Magazine"
        }
    )

def magazines(request):
    pass


def default(request):
    return redirect('home')