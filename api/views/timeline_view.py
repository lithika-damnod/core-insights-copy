from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models.shipment import Shipment
from api.serializers.timeline_serializer import TimelineItemSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from api.models.timeline import TimelineItem

class TimelineView(APIView): 
    permission_classes = [IsAuthenticated]    

    def get(self, request, id): 
        shipment = get_object_or_404(Shipment, id=id)
        timeline_items = shipment.timeline.all()
        serializer = TimelineItemSerializer(timeline_items, many=True)
        return Response(serializer.data)

    def post(self, request, id): 
        shipment = get_object_or_404(Shipment, id=id)

        serializer = TimelineItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shipment=shipment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteTimeLineItemByKey(request, id, key): 
    timelineItem = get_object_or_404(TimelineItem, shipment=id, shipment_sequence=key)
    timelineItem.delete()
    return Response({}, status=status.HTTP_204_NO_CONTENT)