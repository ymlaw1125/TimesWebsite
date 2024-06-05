import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.


class Magazine(models.Model):

    title = models.CharField(max_length=100)
    theme = models.CharField(max_length=100, null=True)
    cover = models.ImageField(upload_to='cover/', null=True, blank=True)
    upload_date = models.DateTimeField(null=True)

    document = models.FileField(upload_to='library/')
    img1 = models.ImageField(upload_to="highlight/")
    img2 = models.ImageField(upload_to="highlight/")
    img3 = models.ImageField(upload_to="highlight/")
    t1 = models.CharField(max_length=300, null=True)
    t2 = models.CharField(max_length=300, null=True)
    t3 = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.title

    def get_verbose_name(self):
        return self.title

    def get_verbose_name_plural(self):
        return self.title

    def get_absolute_url(self):
        return reverse('magazines', args=[self.id])

