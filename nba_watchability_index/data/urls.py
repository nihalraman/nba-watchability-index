from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r"teams", views.TeamViewSet, basename="team")
# router.register(r"cities", views.city_detail)


urlpatterns = [
    path("", include(router.urls)),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    path("cities/", views.CityList.as_view()),
    path("cities/<str:city_name>", views.CityDetail.as_view()),
    path("teams/", views.TeamList.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
