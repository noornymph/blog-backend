"""Configuration settings of our application."""

from django.apps import AppConfig


class BlogappConfig(AppConfig):
    """Application configuration class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blogapp"
