from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=20)
    population = models.IntegerField(default=0)
    # if name is not a real city name (e.g., Golden State),
    # 'actual_city_name' provides real city name (e.g., Golden State maps to San Francisco)
    actual_city_name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    nickname = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city} {self.nickname}"


class Player(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
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
    """Individual game between home team and away team"""

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away")
    date = models.DateField()


class PlayerGameScore(models.Model):
    """Number of points scored by a player in a given game"""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    num_points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )


class Awards(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PlayerAward(models.Model):
    """Player winning an award"""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    award = models.ForeignKey(Awards, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(2100)]
    )
