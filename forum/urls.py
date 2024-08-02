from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
]
