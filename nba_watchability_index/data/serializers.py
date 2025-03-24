from django.contrib.auth.models import User
from rest_framework import serializers

from .models import City, Franchise, Player, Team


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # Include id and name for serialization
        fields = ["id", "name", "actual_city_name", "population"]


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        # Include id and name for serialization
        fields = ["id", "name"]


class TeamSerializer(serializers.ModelSerializer):

    city = serializers.StringRelatedField()
    franchise = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ["team_id", "name", "city", "franchise", "active_team"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "player_id",
            "name",
            "position",
            "height_in",
            "weight",
            "dob",
            "teams",
        ]
