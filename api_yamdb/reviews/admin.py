from django.contrib import admin

from .models import User, Comment, Review

admin.site.register(User)


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
class ReviewAdmin(admin.ModelAdmin):
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
