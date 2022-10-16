from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignupSerializer(serializers.Serializer):
    """
    Сериализатор: регистрация пользователя.
    """

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        """
        Проверяем, что username не равен me.
        """

        if value.lower() == settings.UNUSED_USERNAME:
            raise serializers.ValidationError(
                f'Username не может быть {settings.UNUSED_USERNAME}'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор: получение токена авторизации.
    """

    confirmation_code = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CommentSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации данных Comment.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации Review.
    Проверяет с использованием валидации,
    что при POST запросе от одного пользователя,
    будет создан всего один обзор на одно произведение.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(title_id=title_id, author=author).exists():
            raise ValidationError('Нельзя добавить более одного отзыва')
        return data


class CategorySerializer(serializers.ModelSerializer):
    """
    Серриализация модели Category.
    """

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """
    Серриализация модели Genre.
    """

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Серриализация модели Title для записи.
    """

    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Серриализация модели Title для чтения.
    """

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
