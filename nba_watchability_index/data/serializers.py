from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import City, Player, Team


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # Include id and name for serialization
        fields = ["id", "name", "actual_city_name", "population"]


class TeamSerializer(serializers.ModelSerializer):

    city = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ["nickname", "city"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["player_id", "name", "position", "height_in", "weight", "dob"]
