"""Serializers of the application."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Follow, Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""

    class Meta:
        """Metadata about post serializer."""

        model = Post
        fields = "__all__"
        read_only_fields = ("user",)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    class Meta:
        """Metadata about user serializer."""

        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create a new user with validated data."""
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""

    class Meta:
        """Metadata about follow serializer."""

        model = Follow
        fields = "__all__"
        read_only_fields = ("follower",)
