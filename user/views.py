from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import (get_user_model, logout as django_logout, login as django_login,
                                 authenticate)
from .forms import *
from django.contrib.auth.decorators import login_required
User = get_user_model()


def favorites(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'user_lib.html',
        {
            'title': 'Favorites'
        }
    )


@login_required(login_url='/login/')
def profile(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        return render(request, 'profile.html', {'title': 'Profile'})
    else:
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
        return render(request, 'profile.html', {'title': 'Profile', 'form': form})


@login_required(login_url='/login/')
def reset_password(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        return render(request, 'reset_pwd.html', {'title': 'Reset Password'})
    else:
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            old_pwd = form.cleaned_data.get('old_pwd')
            new_pwd = form.cleaned_data.get('new_pwd')
            if request.user.check_password(old_pwd):
                request.user.set_password(new_pwd)
                request.user.save()
                django_logout(request)
                return redirect(reverse('login'))
            else:
                form.add_error('old_pwd', 'Old password is incorrect')
                return render(request, 'reset_pwd.html', {'title': 'Reset Password', 'form': form})
        else:
            return render(request, 'reset_pwd.html', {'title': 'Reset Password', 'form': form})


def login(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        if request.META.get('HTTP_REFERER') is not None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(reverse('home'))
    if request.method == 'GET':
        return render(request, 'login.html', {'title': 'Log In'})
    else:
        form = LoginForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                django_login(request, user)
                return redirect('home')
            else:
                form.errors['username'] = ['Username or password is incorrect.']
                return render(request, 'login.html', {'title': 'Log In', 'form': form})
        else:
            return render(request, 'login.html', {'title': 'Log In', 'form': form})


@login_required(login_url='/login/')
def logout(request):
    assert isinstance(request, HttpRequest)
    django_logout(request)
    if request.META.get('HTTP_REFERER') is not None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('home'))


def signup(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'GET':
        return render(request, 'signup.html', {'title': 'Sign Up'})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, password=password, email=email)
            return redirect('login')
        else:
            return render(request, 'signup.html', {'title': 'Sign Up', 'form': form})
