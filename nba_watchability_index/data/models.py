from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Team(models.Model):
    nickname = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city} {self.nickname}"


class Player(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team, through="PlayerTeam", related_name="players")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class PlayerTeam(models.Model):
    """Through model to link players with teams and add additional information."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    # Optional, if the player leaves the team
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        # A player can only be in one team at a time for a given period
        unique_together = ("player", "team")


class Game(models.Model):
    home_team_id = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home"
    )
    away_team_id = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away"
    )
    date = models.DateField()


class PlayerGameScore(models.Model):
    """Number of points scored by a player in a given game"""

    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    num_points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
