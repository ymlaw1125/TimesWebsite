from django.urls import path
from . import views

urlpatterns = [
    path('library/', views.library, name='library'),
    path('click_magazines/', views.click_magazines, name='click_magazines')
]