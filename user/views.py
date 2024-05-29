from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import get_user_model
from .form import *

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
    return render(
        request,
        'login.html',
        {
            "title": "Log In"
        }
    )


def logout(request):
    pass


def signup(request):
    assert isinstance(request, HttpRequest)
    if request.method == "GET":
        return render(
            request,
            'signup.html',
            {
                "title": "Sign Up"
            })
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            username_exists = User.objects.filter(username=username).exists()
            if username_exists:
                return JsonResponse({"code": 400,
                                     "message": "Validation failed",
                                     "data": {"username": "Username already exists!",
                                              "password1": "",
                                              "password2": "",
                                              "email": ""}})
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                return JsonResponse({"code": 400,
                                     "message": "Validation failed",
                                     "data": {"username": "",
                                              "password1": "",
                                              "password2": "",
                                              "email": "Email already exists, try logging in."}})
            User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({"code": 200,
                                 "message": "Validation successful",
                                 "data": {"username": "",
                                          "password1": "",
                                          "password2": "",
                                          "email": ""}})
        else:
            return JsonResponse({"code": 400,
                                 "message": "Validation failed",
                                 "data": {"username": form.errors.get("username"),
                                          "password1": form.errors.get("password1"),
                                          "password2": form.errors.get("password2"),
                                          "email": form.errors.get("email")}})
