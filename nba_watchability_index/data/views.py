from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.parsers import JSONParser

from .models import City, Team
from .serializers import CitySerializer, TeamSerializer, UserSerializer

# def index(request):
#     return HttpResponse("Hello, world. You're at the nba index.")


# class CityViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows cities to be viewed or edited.
#     """

#     queryset = City.objects.all()
#     serializer_class = CitySerializer
#     permission_classes = [permissions.IsAuthenticated]


# class TeamViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows teams to be viewed or edited.
#     """

#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     permission_classes = [permissions.IsAuthenticated]


def city_list(request):
    """
    Retrieve all cities, or create a new one.
    """
    if request.method == "GET":
        # Retrieve all cities
        cities = City.objects.all()
        # Serialize all cities
        serializer = CitySerializer(cities, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # Handle city creation (if you want to support creating new cities via POST)
        data = JSONParser().parse(request)
        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Return the created city with a 201 status
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def city_detail(request, city_id):
    """
    Retrieve, update, or delete a specific city.
    """
    try:
        # Retrieve a single city by its ID
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        # Serialize the single city object
        serializer = CitySerializer(city)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        # Parse the incoming JSON data for updates
        data = JSONParser().parse(request)
        serializer = CitySerializer(city, data=data)

        # Check if the data is valid and save it
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        # Delete the city
        city.delete()
        return HttpResponse(status=204)


def team_list(request):
    """
    Retrieve all teams, or create a new one.
    """
    if request.method == "GET":
        # Retrieve all cities
        teams = Team.objects.all()
        # Serialize all cities
        serializer = TeamSerializer(teams, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # Handle city creation (if you want to support creating new cities via POST)
        data = JSONParser().parse(request)
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Return the created city with a 201 status
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
