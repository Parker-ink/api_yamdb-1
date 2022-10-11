from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAdminModeratorAuthorOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer,
    SignupSerializer,
    UserSerializer,
    TokenSerializer,
    UserMePatchSerializer,
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from users.models import User


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():

        user, obj = User.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email'],
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
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
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
            serializer = UserMePatchSerializer(
                instance, user, many=False, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CreateRetrieveViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering_fields = ('name')
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering_fields = ('name')
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
