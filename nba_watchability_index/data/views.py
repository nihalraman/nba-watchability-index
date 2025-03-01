from django.http import HttpResponse

from .models import Team


def index(request):
    return HttpResponse("Hello, world. You're at the nba index.")


def team(request):
    # get associated name for FK city
    allteams = Team.objects.values_list("city__name", "nickname")
    if allteams:
        allteams_html = "<ul>"
        for city_name, nickname in allteams:
            allteams_html += f"<li>Team: {city_name} {nickname}</li>"
        allteams_html += "</ul>"
    else:
        allteams_html = "<p>No teams found.</p>"
    return HttpResponse(allteams_html)
