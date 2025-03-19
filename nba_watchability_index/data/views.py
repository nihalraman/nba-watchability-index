from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import City, Team
from .serializers import CitySerializer, TeamSerializer, UserSerializer


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request),
        }
    )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # restrict to staff users only
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # restrict to staff users only
    permission_classes = [permissions.IsAdminUser]


class CityList(generics.ListAPIView):
    """Retrieve all cities, or create a new one."""

    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDetail(generics.RetrieveAPIView):
    """Retrieve, update, or delete a specific city."""

    queryset = City.objects.all()
    serializer_class = CitySerializer

    lookup_field = "city_name"  # The field to match the string against

    def get_object(self):
        """
        Override the default `get_object` method to retrieve a city by its name.
        """
        city_name = self.kwargs.get(
            self.lookup_field
        )  # Get the city name from URL parameter

        # Perform a case-insensitive lookup, also ignore spaces in city names
        try:
            city = City.objects.get(name__iexact=city_name.replace(" ", ""))
        except City.DoesNotExist:
            raise NotFound(f"City with name '{city_name}' not found.")

        return city


class TeamList(generics.ListCreateAPIView):
    """Retrieve all teams, or create a new one."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveAPIView):
    """Retrieve, update, or delete a specific team."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    lookup_field = "team_nickname"  # The field to match the string against

    def get_object(self):
        """
        Override the default `get_object` method to retrieve a team by its name.
        """
        team_name = self.kwargs.get(
            self.lookup_field
        )  # Get the team name from URL parameter

        # Perform a case-insensitive lookup, also ignore spaces in team names
        try:

            team = Team.objects.get(nickname__iexact=team_name.replace(" ", ""))
        except Team.DoesNotExist:
            raise NotFound(f"Team with name '{team_name}' not found.")

        return team
