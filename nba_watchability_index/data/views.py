from django.http import HttpResponse
from rest_framework import permissions, viewsets

from .models import City, Team
from .serializers import CitySerializer, TeamSerializer, UserSerializer

# def index(request):
#     return HttpResponse("Hello, world. You're at the nba index.")


class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
