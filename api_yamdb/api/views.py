from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from api.serializers import (
    SignupSerializer,
    UserSerializer,
    TokenSerializer,
)
from reviews.models import User
from django.core import mail
from api.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create(
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
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = LimitOffsetPagination
    search_fields = ('username',)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        return get_object_or_404(
            User, username=self.kwargs['username'])


class MeViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return get_object_or_404(
    #         User, username=self.kwargs['username'])
