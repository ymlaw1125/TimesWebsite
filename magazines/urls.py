from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('', views.default, name='default'),
    path('magazines/', views.magazines, name='magazines'),
]