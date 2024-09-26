"""Models of the application."""

from django.db import models
from django.utils.text import slugify


class Categories(models.TextChoices):
    """Model for the categories of blog posts"""

    WORLD = "world"
    ENVIRONMENT = "environment"
    TECHNOLOGY = "technology"
    DESIGN = "design"
    CULTURE = "culture"
    BUSINESS = "business"
    POLITICS = "politics"


class Post(models.Model):
    """Model handling the blog posts."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.CharField(
        max_length=50, choices=Categories.choices, default=Categories.WORLD
    )
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)

    class Meta:
        """Metadata about the Post model."""

        ordering = ["-created"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)
