from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, User
from api.permissions import IsAdmin
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleSerializer,
                             TokenSerializer, UserMePatchSerializer,
                             UserSerializer)
from api.permissions import IsAdmin, IsAuthorOrReadOnly, IsModerator


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():

        user, obj = User.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email'],
            is_active=0,
        )

        confirmation_code = default_token_generator.make_token(user)
        with mail.get_connection() as connection:
            mail.EmailMessage(
                'confirmation_code',
                f"{serializer.data['username']} - {confirmation_code}",
                'as@sdasd.ru',
                [serializer.data['email']],
                connection=connection,
            ).send()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.data['username'])
        confirmation_code = serializer.data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            User.objects.filter(
                username=serializer.data['username']).update(is_active=1)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            user = request.user
            serializer = self.get_serializer(user, many=False)
            return Response(serializer.data)
        if request.method == 'PATCH':
            instance = request.user
            user = request.data
            serializer = UserMePatchSerializer(instance, user, many=False, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdmin, IsModerator]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdmin, IsModerator]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (

    )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer





    #     if serializer.data['username'] == 'me':
    #         return Response(
    #             'Username не может равняться me',
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if User.objects.filter(
    #         username=serializer.data['username'],
    #         email=serializer.data['email']
    #     ).exists():
    #         user = User.objects.filter(
    #             username=serializer.data['username'],
    #             email=serializer.data['email']
    #         )
    #         if user.is_active:
    #             return Response(
    #                 'Username и email уже есть в базе',
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         else:

        
    #     try:
    #         user = User.objects.create(username=serializer.data['username'])
    #     except IntegrityError:
    #         user = User.objects.get(username=serializer.data['username'])
    #         if user.is_active:
    #             return Response(
    #                 'Username уже есть в базе',
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #     if User.objects.filter(email=serializer.data['email']).exists():
    #         user = User.objects.get(email=serializer.data['email'])
    #         if user.is_active:
    #             return Response(
    #                 'Email уже есть в базе',
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #     User.objects.filter(username=serializer.data['username']).update(
    #         is_active=0, email=serializer.data['email'])

    #     confirmation_code = default_token_generator.make_token(user)
    #     with mail.get_connection() as connection:
    #         mail.EmailMessage(
    #             'confirmation_code',
    #             f"{serializer.data['username']} - {confirmation_code}",
    #             'as@sdasd.ru',
    #             [serializer.data['email']],
    #             connection=connection,
    #         ).send()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
