from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Q
from magazines.models import Magazine
from forum.models import Posts


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
    magazine_favorites = models.ManyToManyField(
        to=Magazine,
        related_name='saved_users',
        blank=True
    )
    post_likes = models.ManyToManyField(
        to=Posts,
        related_name='liked_users',
        blank=True
    )
    subscribe = models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    # magazine
    def get_magazine_favorites(self):
        return self.magazine_favorites

    def set_magazine_favorites(self, magazine_favorites):
        self.magazine_favorites = magazine_favorites

    def add_magazine_favorite(self, magazine_id):
        if Magazine.objects.filter(id=magazine_id).exists() and Magazine.objects.get(
                id=magazine_id) not in self.magazine_favorites.all():
            self.magazine_favorites.add(Magazine.objects.get(id=magazine_id))

    def remove_magazine_favorite(self, magazine_id):
        if Magazine.objects.filter(id=magazine_id).exists() and Magazine.objects.get(
                id=magazine_id) in self.magazine_favorites.all():
            self.magazine_favorites.remove(Magazine.objects.get(id=magazine_id))

    def has_magazine_favorited(self, magazine_id):
        print(Magazine.saved_users)
        if Magazine.objects.filter(id=magazine_id).exists() and Magazine.objects.get(
                id=magazine_id) in self.magazine_favorites.all():
            return True
        else:
            return False
        
    # posts    
    def get_post_likes(self):
        return self.post_likes

    def set_post_likes(self, post_likes):
        self.post_likes = post_likes

    def add_post_like(self, post_id):
        if Posts.objects.filter(id=post_id).exists() and Posts.objects.get(
                id=post_id) not in self.post_likes.all():
            self.post_likes.add(Posts.objects.get(id=post_id))

    def remove_post_like(self, post_id):
        if Posts.objects.filter(id=post_id).exists() and Posts.objects.get(
                id=post_id) in self.post_likes.all():
            self.post_likes.remove(Posts.objects.get(id=post_id))

    def has_post_liked(self, post_id):
        print(Posts.liked_users)
        if Posts.objects.filter(id=post_id).exists() and Posts.objects.get(
                id=post_id) in self.post_likes.all():
            return True
        else:
            return False

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
