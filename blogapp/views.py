"""Views of the application."""

from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Categories, Favorite, Follow, Post
from .serializers import (
    FollowSerializer,
    LoginSerializer,
    PostSerializer,
    UserSerializer,
)


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

    @action(detail=False, methods=["get"], url_path="category/(?P<category>[^/.]+)")
    def by_category(self, request, category=None):
        """Filter posts by category"""
        if category not in Categories.values:
            return Response({"error": "Invalid category"}, status=400)

        posts = self.queryset.filter(category=category)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        """Add a blog post to the user's favorites."""
        post = self.get_object()
        Favorite.objects.get_or_create(user=request.user, post=post)
        return Response({"status": "post favorited"})


class FollowView(viewsets.ModelViewSet):
    """View for handling follow relationships between users."""

    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        """Save a new follow instance with the authenticated user."""
        serializer.save(follower=self.request.user)


class LoginView(generics.GenericAPIView):
    """Viewset for handling user login."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """Handles the POST request for user login."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
