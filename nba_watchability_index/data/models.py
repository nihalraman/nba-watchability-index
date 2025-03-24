from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=40)
    population = models.IntegerField(null=True)
    # if name is not a real city name (e.g., Golden State),
    # 'actual_city_name' provides real city name (e.g., Golden State maps to San Francisco)
    actual_city_name = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


class Franchise(models.Model):
    """Correspond to unique basketball reference franchises. Name defaults to current team name if available."""

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Team(models.Model):
    team_id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=40)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    active_team = models.BooleanField()

    def __str__(self):
        return f"{self.city} {self.name}"


class Player(models.Model):
    # set pk as charfield so we can use bbref IDs
    player_id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=40)
    position = models.CharField(max_length=10)
    height_in = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(500)], null=True
    )
    dob = models.DateTimeField(null=True)
    teams = models.ManyToManyField(Team, through="PlayerTeam", related_name="players")

    def __str__(self):
        return f"{self.name}"


class PlayerTeam(models.Model):
    """Through model to link players with teams and add additional information."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    first_game = models.DateField()
    # Optional, if the player leaves the team
    last_game = models.DateField(null=True)

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
