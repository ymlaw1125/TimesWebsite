from django.urls import path
from . import views

urlpatterns = [
    # TODO add profile path
    path('favorites/', views.favorites, name='favorites'),
]