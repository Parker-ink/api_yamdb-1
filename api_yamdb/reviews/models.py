from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from users.models import User


class Category(models.Model):
    """
    Модель для создания категории (типа) произведений.
    """

    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель для создания жанров произведений.
    """

    name = models.CharField(
        verbose_name="Название",
        max_length=256
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель для создания произведений, к которым пишут отзывы.
    """

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name='categories'
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        related_name='genre',
        through="GenreTitle"
    )
    name = models.CharField(
        verbose_name="Название",
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год создания",
        validators=(
            MinValueValidator(1500, 'значение должно быть больше 1500'),
            MaxValueValidator(
                now().year, 'значение должно быть меньше текущего года'
            )
        )
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


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
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            ),
        )

    def __str__(self):
        return self.text[:settings.CONFINES_TEXT]


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
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:settings.CONFINES_TEXT]
