from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Представление юзеров в админ-панели.
    """

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'bio',
        'role',
        'is_active'
    )
    list_filter = ('is_active', 'role')
    search_fields = ('username', 'email')
