from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import (get_user_model, logout as django_logout, login as django_login,
                                 authenticate)
from .forms import *

User = get_user_model()


def favorites(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'user_lib.html',
        {
            "title": "Favorites"
        }
    )


def login(request):
    assert isinstance(request, HttpRequest)
    if request.method == "GET":
        return render(request, 'login.html', {"title": "Log In"})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                django_login(request, user)
                request.session['username'] = user.username
                return redirect('home')
            elif user and not user.is_active:
                # TODO add login error message to template
                return JsonResponse({"code": 400,
                                     "message": "user not active",
                                     "data": {"error": "user not active"}
                                     })
            else:
                # TODO add login error message to template
                return JsonResponse({"code": 400,
                                     "message": "username or password incorrect",
                                     "data": {"error": "username or password incorrect"}
                                     })
        else:
            # TODO add error message to template
            return JsonResponse(form.errors, safe=False)


def logout(request):
    assert isinstance(request, HttpRequest)
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def signup(request):
    assert isinstance(request, HttpRequest)
    if request.method == "GET":
        return render(request, 'signup.html', {"title": "Sign Up"})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            User.objects.create_user(username=username, password=password, email=email)
            return redirect("login")
        else:
            # TODO add error message to template
            return JsonResponse(form.errors, safe=False)
