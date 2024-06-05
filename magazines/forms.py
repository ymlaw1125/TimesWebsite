from django import forms
from django.core.exceptions import ValidationError

from .models import Magazine
from django.db import models
from datetime import datetime
import os

class MagazineForm(forms.ModelForm):

    title = models.CharField(max_length=100)
    theme = models.CharField(max_length=100, blank=True)
    cover = models.ImageField(upload_to='cover/', blank=True)
    upload_date = models.DateTimeField()

    document = models.FileField(upload_to='library/')
    img1 = models.ImageField(upload_to="highlight/")
    img2 = models.ImageField(upload_to="highlight/")
    img3 = models.ImageField(upload_to="highlight/")
    t1 = models.CharField(max_length=200)
    t2 = models.CharField(max_length=200)
    t3 = models.CharField(max_length=200)

    class Meta:
        model = Magazine
        fields = "__all__"
