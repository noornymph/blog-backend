"""Admin panel settings of the application."""

from django.contrib import admin

from .models import Post

# Register your models here.

admin.site.register(Post)
