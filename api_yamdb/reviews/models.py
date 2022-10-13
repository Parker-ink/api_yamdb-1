from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now


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

    def __str__(self):
        return self.username


class Category(models.Model):
    """
    Модель для создания категории (типа) произведений.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True
    )


class Genre(models.Model):
    """
    Модель для создания жанров произведений.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True
    )


class Title(models.Model):
    """
    Модель для создания произведений, к которым пишут отзывы.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    description = models.TextField(
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre'
    )
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(validators=(
        MinValueValidator(1500, 'значение должно быть больше 1500'),
        MaxValueValidator(now().year, 'значение должно быть меньше текущего года')
    ))


class Review(models.Model):
    """
    Модель для создания обзора для произведения.
    """
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
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=(
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        )
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для создания комментария на обзоры произведений.
    """
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
