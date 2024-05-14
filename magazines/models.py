from django.db import models
import django


# Create your models here.
class Magazine(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    upload_time = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='static/documents/')
