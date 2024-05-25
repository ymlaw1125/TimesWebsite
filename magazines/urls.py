from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('magazine/', views.click_magazines, name='click_magazines')]