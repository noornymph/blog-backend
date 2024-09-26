"""URL configuration for yt_blog_api project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("", include("blogapp.urls"))]
