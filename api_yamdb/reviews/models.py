from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )    
    bio = models.TextField(
        'Биография',
        blank=True,
    ) 
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLES,
    ) 

    def __str__(self):
        return self.username
