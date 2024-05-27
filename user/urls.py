from django.urls import path
from . import views

urlpatterns = [
    path('library/', views.library, name='library'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]