"""URL paths of our application."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("blogs", views.PostModelViewSet)
router.register("follow", views.FollowView, basename="follow")

urlpatterns = [
    path("", include(router.urls)),
    path("users/signup/", views.UserRegisterView.as_view(), name="user-register"),
    path(
        "blogs/category/<slug:category_slug>/",
        views.PostModelViewSet.as_view({"get": "by_category"}),
        name="blog-by-category",
    ),
    path("users/login/", views.LoginView.as_view(), name="login"),
]
