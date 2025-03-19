from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path("", views.api_root),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("cities/", views.CityList.as_view(), name="city-list"),
    path("cities/<str:city_name>/", views.CityDetail.as_view(), name="city-detail"),
    path("teams/", views.TeamList.as_view(), name="team-list"),
    path("teams/<str:team_nickname>/", views.TeamDetail.as_view(), name="team-detail"),
]

# add auth
urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
