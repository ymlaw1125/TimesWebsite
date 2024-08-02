from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def forum(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'forum_main.html', {"title": "Home"})
