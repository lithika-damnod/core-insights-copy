from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsMerchant
from api.serializers.shipment_serializer import ShipmentSerializer
from rest_framework import status
from api.models.user import MerchantAdministrator

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
        

