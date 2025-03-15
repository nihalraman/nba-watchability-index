from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import City, Team
from .serializers import CitySerializer, TeamSerializer, UserSerializer

# def index(request):
#     return HttpResponse("Hello, world. You're at the nba index.")


# class CityViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows cities to be viewed or edited.
#     """

#     queryset = City.objects.all()
#     serializer_class = CitySerializer
#     permission_classes = [permissions.IsAuthenticated]


# class TeamViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows teams to be viewed or edited.
#     """

#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     permission_classes = [permissions.IsAuthenticated]


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
        for city in self.get_queryset():
            if city.name.lower().replace(" ", "") == city_name.lower():
                return city

        # if no city found, raise exception
        raise NotFound(f"City with name '{city_name}' not found.")


class TeamList(generics.ListCreateAPIView):
    """Retrieve all teams, or create a new one."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
