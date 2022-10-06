from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = 'name', 'slug'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')