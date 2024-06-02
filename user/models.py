from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Q
from magazines.models import Magazine


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("Please enter your username")
        if not password:
            raise ValueError("Please enter your password")
        if not email:
            raise ValueError("Please enter your email address")
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
    favorites = models.ManyToManyField(to=Magazine,
                                       related_name='saved_users',
                                       blank=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_favorites(self):
        return self.favorites

    def set_favorites(self, favorites):
        self.favorites = favorites

    def add_favorite(self, magazine_id):
        if (Magazine.objects.filter(id=magazine_id).exists() and magazine_id not in
                self.favorites['id']):
            self.favorites['id'].append(magazine_id)

    def remove_favorite(self, magazine_id):
        if Magazine.objects.filter(id=magazine_id).exists() and magazine_id in self.favorites['id']:
            self.favorites['id'].remove(magazine_id)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


from django.contrib.auth.backends import AllowAllUsersModelBackend


class CustomUserBackend(AllowAllUsersModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        user = CustomUser.objects.filter(Q(username=username) | Q(email=username)).first()
        if user:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return
