from django.db import models

# Create your models here.
class savedLibrary(models.model):
    user_id = models.IntegerField()
    saved_magazines = models.JSONField()
    saved_count = models.IntegerField()
