from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Favorites, Profile
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
def get_favorites_details(request, to_address):
    try:
        # Fetch all favorites for the given address
        favorites = list(Favorites.objects.filter(to_address=to_address))
        if not favorites:
            return Response({"detail": "No favorites found for this address."}, status=status.HTTP_404_NOT_FOUND)
        
        # Extract profile addresses
        profile_addresses = [fav.from_address for fav in favorites]
        
        # Query the Profile model using the unique addresses
        profiles = Profile.objects.filter(address__in=profile_addresses)
        serializer = ProfileSerializer(profiles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
