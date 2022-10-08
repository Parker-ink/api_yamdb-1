from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UsersViewSet, get_token,
                       signup)

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')


urlpatterns = [
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
