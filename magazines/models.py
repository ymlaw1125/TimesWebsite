from django.db import models
from django.utils import timezone


# Create your models here.
class Magazine(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    upload_time = models.DateTimeField()
    document = models.FileField(upload_to='media/library/')
