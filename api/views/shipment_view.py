from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsMerchant
from api.serializers.shipment_serializer import ShipmentSerializer
from rest_framework import status
from api.models.user import MerchantAdministrator
from rest_framework.decorators import api_view
from api.models.shipment import Shipment
from django.shortcuts import get_object_or_404

class ShipmentView(APIView): 
    def get_permissions(self):
        if self.request.method == "POST": 
            return [IsAuthenticated(), IsMerchant()]
        return [IsAuthenticated()] 
         

    def get(self, request): 
        return Response({"detail": "anyone allowed here.."})

    def post(self, request): 
        serializer = ShipmentSerializer(data=request.data)

        if serializer.is_valid(): 
            merchant = MerchantAdministrator.objects.get(id=request.user.id)
            shipment = serializer.save(merchant=merchant)
            return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_tracking_no_validity(request): 
    tracking_no = str(request.GET.get('id', None)).upper()

    
    if not tracking_no: 
        return Response({'detail': 'id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    tracking_no_exists = Shipment.objects.filter(id=tracking_no).exists() 


    return Response({
        'validity': tracking_no_exists,
        'detail':  'Valid Tracking Number' if tracking_no_exists else 'Invalid Tracking Number'
    })    


class ShipmentById(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, id): 
        shipment = Shipment.objects.filter(id=str(id)).first()
        if not shipment: 
            return Response({"detail": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)

    def delete(self, request, id): 
        shipment = get_object_or_404(Shipment, id=id)
        shipment.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)



