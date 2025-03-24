from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import City, Franchise, Player, Team
from .serializers import (
    CitySerializer,
    FranchiseSerializer,
    PlayerSerializer,
    TeamSerializer,
    UserSerializer,
)


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "users": reverse("user-list", request=request),
        }
    )


class UserViewSet(ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CityViewSet(ModelViewSet):
    """Retrieve, create, update, or delete cities."""

    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = "city_name"  # Use `city_name` as the lookup field

    def get_object(self):
        """
        Override the default `get_object` method to retrieve a city by its name.
        """
        city_name = self.kwargs.get(
            self.lookup_field
        )  # Get the city name from URL parameter

        # Perform a case-insensitive lookup, also ignore spaces in city names
        try:
            city = City.objects.get(name__iexact=city_name.title())
        except City.DoesNotExist:
            raise NotFound(f"City with name '{city_name}' not found.")

        return city


class FranchiseViewSet(ModelViewSet):
    """Retrieve, create, update, or delete franchises."""

    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer


class TeamViewSet(ModelViewSet):
    """Retrieve, create, update, or delete a specific team."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "team_nickname"  # Use `team_nickname` as the lookup field

    def get_object(self):
        """
        Override the default `get_object` method to retrieve a team by its nickname.
        """
        team_nickname = self.kwargs.get(
            self.lookup_field
        )  # Get the team nickname from URL parameter

        # Perform a case-insensitive lookup, also ignore spaces in team nicknames
        try:
            team = Team.objects.get(nickname__iexact=team_nickname.title())
        except Team.DoesNotExist:
            raise NotFound(f"Team with nickname '{team_nickname}' not found.")

        return team


class PlayerViewSet(ModelViewSet):
    """Retrieve, create, update, or delete a specific player."""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
