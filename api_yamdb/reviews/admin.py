from django.contrib import admin

from reviews.models import Category, Genre, Title, Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Представление Обзоров в админ-панели.
    """

    list_display = (
        'text',
        'author',
        'title',
        'pub_date',
        'score',
    )
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Представление Комментариев в админ-панели.
    """

    list_display = (
        'text',
        'review',
        'author',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('pub_date',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """
    Представление произведений в админке.
    """

    list_display = (
        'id',
        'name',
        'year',
        'category'
    )
    search_fields = ('name', 'description')
    list_filter = ('name', 'year',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Представление жанров в админке.
    """

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Представление категорий в админке.
    """

    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
