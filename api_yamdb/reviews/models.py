from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERUSER = 1
    USER_ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )
    email = models.EmailField(
        'email address',
        unique=True
    )

    def __str__(self):
        return self.username

    # def is_admin(self):
    #     return (
    #         self.role == ADMIN
    #     )

    # def is_moderator(self):
    #     return (
    #         self.role == MODERATOR
    #     )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField()


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ['pub_date']


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ['pub_date']


"""
class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("Ip адрес клиента", max_length=69)
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name='Звезда'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
"""
