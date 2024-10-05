from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from .models import Posts, Comments, Vote
from django.conf import settings


class PostsForm(forms.ModelForm):
    title = models.CharField(max_length=300)
    text = models.CharField(max_length=10000, null=True, blank=True)
    community = models.CharField(max_length=300)
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)

    class Meta:
        model = Posts
        fields = "__all__"


class CommentsForm(forms.ModelForm):
    message = models.CharField(max_length=10000)
    post = models.ForeignKey(to=Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)

    class Meta:
        model = Comments
        fields = "__all__"


class VoteForm(forms.ModelForm):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='votes', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, related_name='votes', null=True, blank=True, on_delete=models.CASCADE)
    vote_type = models.BooleanField()

    class Meta:
        model = Vote
        fields = "__all__"