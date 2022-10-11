from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


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
        on_delete=models.PROTECT,
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
    year = models.IntegerField(default='2000')


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
        auto_now_add=True
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
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


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
