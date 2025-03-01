from django.http import HttpResponse

from .models import Team


def index(request):
    return HttpResponse("Hello, world. You're at the nba index.")


def team(request, team_name):
    cur_team = Team.objects.get(nickname=team_name)
    return HttpResponse("You're looking at the %s." % cur_team.__str__())
