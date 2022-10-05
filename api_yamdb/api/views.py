from rest_framework import viewsets

from reviews.models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAdmin, IsAuthorOrReadOnly, IsModerator


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdmin, IsModerator]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdmin, IsModerator]
