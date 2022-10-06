from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views
# from api.views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

app_name = 'api'

# router_v1 = routers.DefaultRouter()
# router_v1.register(
#     r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
# router_v1.register(r'posts', PostViewSet, basename='posts')
# router_v1.register(r'groups', GroupViewSet, basename='groups')
# router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(
        'v1/users/', views.UsersViewSet,
        name='users'
    ),
    path(
        'v1/auth/signup/', views.signup,
        name='signup'
    ),
    path(
        'v1/auth/token/', views.get_token,
        name='token'
    ),
    # path('v1/', include(router_v1.urls))
]
