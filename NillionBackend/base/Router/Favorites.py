from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Favorites
from base.profiles.serializers import FavoritesSerializer, ProfileSerializer


@api_view(['POST'])
def create_favorite(request):
    serializer = FavoritesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_favorites(request):
    favorites = Favorites.objects.all()
    serializer = FavoritesSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_favorite(request, to_address):
    try:
        favorite = Favorites.objects.get(to_address=to_address)
    except Favorites.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FavoritesSerializer(favorite)
    return Response(serializer.data)

@api_view(['PUT'])
def update_favorite(request, to_address):
    try:
        favorite = Favorites.objects.get(to_address=to_address)
    except Favorites.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FavoritesSerializer(favorite, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_favorite(request, to_address):
    try:
        favorite = Favorites.objects.get(to_address=to_address)
    except Favorites.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    favorite.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_favorites_details(request, address):
    try:
        favorites = Favorites.objects.filter(to_address=address)
        if not favorites.exists():
            return Response({"detail": "No favorites found for this address."}, status=status.HTTP_404_NOT_FOUND)
        
        profile_addresses = [fav.from_address for fav in favorites]
        profiles = Profile.objects.filter(address__in=profile_addresses)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)