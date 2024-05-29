from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("Please enter your username")
        if not password:
            raise ValueError("Please enter your password")
        if not email:
            raise ValueError("Please enter your email address")
        kwargs['favorites'] = {'id': []}
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)

        user.save()
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_staff(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, **kwargs)


# Create your models here.
class CustomUser(AbstractUser):
    favorites = models.JSONField(default=dict)
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def get_favorites(self):
        return self.favorites

    def set_favorites(self, favorites):
        self.favorites = favorites

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
