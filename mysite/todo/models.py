from django.db import models
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, password=None):

        if username is None:
            raise TypeError('Users must have a username.')


        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days = 10)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Task(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    completion = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='tasks',  on_delete=models.CASCADE)

    objects = UserManager()

    def __str__(self):
        return self.title
