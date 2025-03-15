from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import City, Team


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # Include id and name for serialization
        fields = ["id", "name", "actual_city_name", "population"]


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    city = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ["nickname", "city"]
