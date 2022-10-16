from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UsersViewSet,
    get_token,
    signup
)

router_v1 = SimpleRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='titles')

auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('', include(router_v1.urls)),
]
