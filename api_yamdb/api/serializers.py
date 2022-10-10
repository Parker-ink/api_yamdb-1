from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        """
        Проверяем username на уникальность.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Такой username уже зарегистрирован")
        if value == 'me':
            raise serializers.ValidationError(
                "Username не может быть me")
        return value

    def validate_email(self, value):
        """
        Проверяем email на уникальность.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Такой email уже зарегистрирован")
        return value


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150)


class UserMePatchSerializer(serializers.Serializer):
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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


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

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance

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

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Нельзя добавить более одного отзыва')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'description', 'genre', 'category')
