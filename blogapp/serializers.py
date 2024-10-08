"""Serializers of the application."""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Follow, Post


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object to include in PostSerializer."""

    class Meta:
        """Metadata about the user serializer."""

        model = User
        fields = ["id", "username"]  # Include id and username


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""

    user = UserSerializer(read_only=True)  # Use the UserSerializer for the user field

    class Meta:
        """Metadata about the post serializer."""

        model = Post
        fields = "__all__"
        read_only_fields = ("user",)


class LoginSerializer(serializers.Serializer):
    """Serializer for the login."""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        raise NotImplementedError(
            "This serializer is for login and does not create a user."
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    class Meta:
        """Metadata about user registration serializer."""

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
