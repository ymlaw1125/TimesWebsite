from django.db import models


# Create your models here.
class UserLib(models.Model):
    user_id = models.IntegerField()
    saved_magazines = models.JSONField()
    saved_count = models.IntegerField()
