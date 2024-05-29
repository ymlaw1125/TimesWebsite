from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name='library'),
    path('<int:magazine_id>', views.magazine, name='magazine'),
]
