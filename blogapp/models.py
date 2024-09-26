"""Models of the application."""

from django.contrib.auth.models import User
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
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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


class Favorite(models.Model):
    """Model representing a user's favorite blog post."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        """Meta options for the Favorite model."""

        unique_together = ("user", "post")

    def __str__(self):
        """String representation of the Favorite model."""
        return f"{self.user.username} favorited {self.post.title}"


class Follow(models.Model):
    """Model representing a follow relationship between users."""

    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        """Meta options for the Follow model."""

        unique_together = ("follower", "followed")

    def __str__(self):
        """String representation of the Follow model."""
        return f"{self.follower.username} follows {self.followed.username}"
