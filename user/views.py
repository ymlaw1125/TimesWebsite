import json

from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import (get_user_model, logout as django_logout, login as django_login,
                                 authenticate)
from .forms import *
from django.contrib.auth.decorators import login_required
User = get_user_model()


@login_required(login_url='/login/')
def favorites(request, username):
    assert isinstance(request, HttpRequest)
    viewed_user = CustomUser.objects.filter(username=username).first()
    if viewed_user is None:
        return render(
            request, 'error.html', {
                'title': 'User does not exist',
                'error_msg': 'Oops... user does not exist'
            }
        )
    searched = ''
    favorite = viewed_user.magazine_favorites.all()
    print(favorite)
    if request.method == 'GET':
        if request.GET.get("form_type") == 'search':
            query = request.GET['query']
            if len(query) != 0:
                searched = query
                query_in_list = query.split()
                to_ignore = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to', 'was', 'will', 'with']
                filtered_query = [e for e in query_in_list if e not in to_ignore]
                results = []
                for item in filtered_query:
                    mags = favorite.filter(
                        Q(title__icontains=item)
                    )
                    for mag in mags:
                        if mag not in results:
                            results.append(mag)
                favorite = results
    return render(
        request,
        'user_lib.html',
        {
            'title': 'Favorites',
            "favorites": favorite,
            "searched": searched
        }
    )


@login_required(login_url='/login/')
def profile(request, username):
    assert isinstance(request, HttpRequest)
    viewed_user = CustomUser.objects.filter(username=username).first()
    if request.method == 'GET':
        return render(request, 'profile.html', {'title': 'Profile', 'viewed_user': viewed_user})
    else:
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
        return render(request, 'profile.html', {'title': 'Profile', 'form': form, 'viewed_user': viewed_user})


@login_required(login_url='/login/')
def reset_password(request):
    assert isinstance(request, HttpRequest)
    viewed_user = CustomUser.objects.filter(username=request.user.username).first()
    if request.method == 'GET':
        return render(request, 'reset_pwd.html', {'title': 'Reset Password', 'viewed_user': viewed_user})
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
            return render(request, 'reset_pwd.html', {'title': 'Reset Password', 'form': form, 'viewed_user': viewed_user})


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
        print(request.META.get("HTTP_REFERER"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('home'))


def signup(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        if request.META.get('HTTP_REFERER') is not None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(reverse('home'))
    if request.method == 'GET':
        return render(request, 'signup.html', {'title': 'Sign Up'})
    else:
        form = SignupForm(request.POST)
        if 'subscribe' not in request.POST:
            subscribe = False
        else:
            subscribe = True
        if form.is_valid():
            print(form)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email, subscribe=subscribe)
            return redirect('login')
        else:
            print(form)
            return render(request, 'signup.html', {'title': 'Sign Up', 'form': form})
