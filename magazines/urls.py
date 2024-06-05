from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from . import views

urlpatterns = [
    path('', views.library, name='library'),
    path('<int:magazine_id>', views.magazine, name='magazine'),
    path('<int:magazine_id>/favorite', views.MagazineFavoriteView.as_view(), name="magazine_favorite")
]
