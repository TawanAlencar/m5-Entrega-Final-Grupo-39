from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_colaborator = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_follow = models.ManyToManyField('books.Book', related_name='users')