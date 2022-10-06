from rest_framework import serializers

from reviews.models import User, Comment, Review, Category, Genre, Title

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        """
        Проверяем, что username != 'me' и на уникальность.
        """
        if value == 'me':
            raise serializers.ValidationError(
                'username не может равняться me')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Такой username уже зарегистрирован')
        return value

    def validate_email(self, value):
        """
        Проверяем email на уникальность.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован')
        return value


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(
        choices=['user', 'moderator', 'admin'],
        default='user',
        required=False
    )

    def validate_username(self, value):
        """
        Проверяем username на уникальность.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Такой username уже зарегистрирован")
        return value

    def validate_email(self, value):
        """
        Проверяем email на уникальность.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Такой email уже зарегистрирован")
        return value

class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
