from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import (get_user_model, logout as django_logout, login as django_login,
                                 authenticate)
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required(login_url='/login/')
def profile(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'profile.html',
        {
            "title": "Profile"
        }
    )

@login_required(login_url='/login/')
def resetpassword(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'reset_pwd.html',
        {
            "title": "Reset Password"
        }
    )


def login(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return redirect('/')
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
            else:
                form.errors['username'] = ["Username or password is incorrect."]
                return render(request, 'login.html', {"title": "Log In", "form": form})
        else:
            return render(request, 'login.html', {"title": "Log In", "form": form})


def logout(request):
    assert isinstance(request, HttpRequest)
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def signup(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return redirect('/')
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
            return render(request, 'signup.html', {"title": "Sign Up", "form": form})
