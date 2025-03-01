from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("teams/<int:team_name>/", views.team, name="team"),
]
