from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Rejectd
from base.profiles.serializers import RejectdSerializer
import uuid

@api_view(['POST'])
def create_rejectd(request):
    serializer = RejectdSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_rejectd(request):
    rejectds = Rejectd.objects.all()
    serializer = RejectdSerializer(rejectds, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_rejectd(request, id):
    try:
        rejectd = Rejectd.objects.get(id=id)
    except Rejectd.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RejectdSerializer(rejectd)
    return Response(serializer.data)

@api_view(['PUT'])
def update_rejectd(request, id):
    try:
        rejectd = Rejectd.objects.get(id=id)
    except Rejectd.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RejectdSerializer(rejectd, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_rejectd(request, id):
    try:
        rejectd = Rejectd.objects.get(id=id)
    except Rejectd.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    rejectd.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
