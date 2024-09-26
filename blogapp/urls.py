"""URLs of the application."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("blogs", views.PostModelViewSet)
router.register("follow", views.FollowView, basename="follow")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
]
