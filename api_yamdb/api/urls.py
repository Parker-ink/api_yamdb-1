from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import ReviewViewSet, CommentViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
