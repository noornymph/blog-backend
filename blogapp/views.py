"""Views of the application."""

from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Favorite, Follow, Post
from .serializers import FollowSerializer, PostSerializer, UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """API view for user registration."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Save a new user instance after validating the serializer."""
        serializer.save()


class PostModelViewSet(ModelViewSet):
    """Viewset for handling blog posts."""

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Save a new post instance with the authenticated user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["GET"])
    def recent(self, request):
        """Function for accessing the recent posts, optionally filtered by category."""
        category = request.query_params.get("category", None)
        if category:
            posts = Post.objects.filter(category=category).order_by("-created")[:6]
        else:
            posts = Post.objects.all().order_by("-created")[:6]

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def by_category(self, request):
        """Function for accessing posts by category."""
        category = request.query_params.get("category")
        if category:
            posts = Post.objects.filter(category=category)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Category not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        """Add a blog post to the user's favorites."""
        post = self.get_object()
        Favorite.objects.get_or_create(user=request.user, post=post)
        return Response({"status": "post favorited"})


class FollowView(viewsets.ModelViewSet):
    """API view for handling follow relationships between users."""

    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer  # You will need to create this serializer

    def perform_create(self, serializer):
        """Save a new follow instance with the authenticated user."""
        serializer.save(follower=self.request.user)
