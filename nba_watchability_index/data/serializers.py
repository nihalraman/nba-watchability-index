from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import City, Team


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
