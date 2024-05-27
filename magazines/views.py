from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def home(request):
    return render(request, 'user_lib.html')


def magazines(request):
    pass


def default(request):
    return redirect('home')