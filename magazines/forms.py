from django import forms
from .models import Magazine
from django.db import models
from datetime import datetime


class MagazineForm(forms.ModelForm):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='cover/', null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='library/')

    class Meta:
        model = Magazine
        fields = "__all__"
