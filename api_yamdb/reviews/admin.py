from django.contrib import admin

from .models import Category, Genre, Title, User

admin.site.register(User)


class TitleAdmin(admin.ModelAdmin):
    """
    Регистрация модели Title в админке.
    """

    list_display = (
        'id', 'name', 'year',
        'category'
    )
    search_fields = ('name', 'description')
    list_filter = ('name', 'year',)

admin.site.register(Title, TitleAdmin)

class GenreAdmin(admin.ModelAdmin):
    """
    Регистрация модели Genre в админке.
    """

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)

admin.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    """
    Регистрация модели Category в админке.
    """

    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(Category, CategoryAdmin)
