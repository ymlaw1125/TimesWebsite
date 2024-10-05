from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('popular/', views.popular, name='popular'),
    path('submit/', views.submit, name='submit'),
    path('<str:community_name>/', views.community, name='community'),
    path('<str:community_name>/<int:post_id>', views.post, name='post'),
    path('vote/post/<int:post_id>/<int:vote_type>/', views.vote_post, name='vote_post'),
    path('vote/comment/<int:comment_id>/<int:vote_type>/', views.vote_comment, name='vote_comment'),
]