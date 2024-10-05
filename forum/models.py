from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.conf import settings


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    text = models.CharField(max_length=10000, blank=True, default='')
    community = models.CharField(max_length=300)
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)
    views = models.IntegerField(default=0, blank=True)


    @property
    def popularity(self):
        return 0.5*self.upvotes + 0.3*self.comments + 0.2*self.views - 0.1*(datetime.now().date() - datetime.date(self.upload_date)).days

    def __str__(self):
        return self.title

    def get_verbose_name(self):
        return self.title

    def get_verbose_name_plural(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts', args=[self.id])


class Comments(models.Model):
    message = models.CharField(max_length=10000)
    post = models.ForeignKey(to=Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"Comment by {self.user_id} on {self.post_id}"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='votes', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, related_name='votes', null=True, blank=True, on_delete=models.CASCADE)
    vote_type = models.BooleanField()

    class Meta:
        unique_together = ('user', 'post', 'comment')
