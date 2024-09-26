"""Views of the application."""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostModelViewSet(ModelViewSet):
    """View of the Post model."""

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"

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
