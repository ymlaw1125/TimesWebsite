from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Magazine(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='cover', blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='library/')

    def __str__(self):
        return self.title

    def get_verbose_name(self):
        return self.title

    def get_verbose_name_plural(self):
        return self.title

    def get_absolute_url(self):
        return reverse('magazines', args=[self.id])

