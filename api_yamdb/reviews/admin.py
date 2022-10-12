from django.contrib import admin

from .models import User, Comment, Review

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
