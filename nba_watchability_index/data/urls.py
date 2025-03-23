from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"cities", views.CityViewSet, basename="city")
router.register(r"teams", views.TeamViewSet, basename="team")
router.register(r"players", views.PlayerViewSet, basename="player")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
