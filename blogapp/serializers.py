"""Serializers of the application."""

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""

    class Meta:
        """Metadata about post serializer."""

        model = Post
        fields = ["id", "title", "content", "slug"]


# get_recent_blogs = http://127.0.0.1:8008/blogs/recent
# sepecific_blog = http://127.0.0.1:8008/blogs/:slug
