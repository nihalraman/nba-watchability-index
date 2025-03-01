from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r"teams", views.TeamViewSet, basename="team")
# router.register(r"cities", views.city_detail)


urlpatterns = [
    path("", include(router.urls)),
    path("cities/", views.city_list),
    path("teams/", views.team_list),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
