from django.http import HttpResponse
from rest_framework import permissions, viewsets

from .models import Team
from .serializers import GroupSerializer, TeamSerializer, UserSerializer

# def index(request):
#     return HttpResponse("Hello, world. You're at the nba index.")


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
