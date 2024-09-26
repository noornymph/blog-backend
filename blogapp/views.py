"""Views of the application."""

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
        """Function for accessing the recent posts."""
        posts = Post.objects.all()[:6]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
