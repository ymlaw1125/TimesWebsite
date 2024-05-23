from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    favorites = models.JSONField(default=dict)

    def __str__(self):
        return self.username

