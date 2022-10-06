from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UsersViewSet,
    signup,
    get_token,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path(
        'v1/users/', UsersViewSet,
        name='users'
    ),
    path(
        'v1/auth/signup/', signup,
        name='signup'
    ),
    path(
        'v1/auth/token/', get_token,
        name='token'
    ),
    path('v1/', include(router_v1.urls)),
]
