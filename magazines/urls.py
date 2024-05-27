from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name='default'),
    path('home/', views.home, name='home'),
    path('magazine/', views.click_magazines, name='click_magazines'),
]