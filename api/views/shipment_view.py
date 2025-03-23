from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsMerchant
from api.serializers.shipment_serializer import ShipmentSerializer, ShipmentBriefSerializer
from rest_framework import status
from api.models.user import MerchantAdministrator, StandardUser, LogisticsAdministrator, Driver
from rest_framework.decorators import api_view
from api.models.shipment import Shipment
from api.models.address import Address
from django.shortcuts import get_object_or_404

class ShipmentView(APIView): 
    def get_permissions(self):
        if self.request.method == "POST": 
            return [IsAuthenticated(), IsMerchant()]
        return [IsAuthenticated()] 
         

    def get(self, request): 
        user = request.user

        if user.is_standard():
            customer = StandardUser.objects.get(id=user.id)
            shipments = Shipment.objects.filter(customer=customer)
        elif user.is_merchant():
            merchant = MerchantAdministrator.objects.get(id=user.id)
            shipments = Shipment.objects.filter(merchant=merchant)
        elif user.is_logistics():
            logistics = LogisticsAdministrator.objects.get(id=user.id)
            shipments = Shipment.objects.filter(logistics=logistics)
        elif user.is_driver():
            driver = Driver.objects.get(id=user.id)
            shipments = Shipment.objects.filter(driver=driver)
        else:
            return Response({"detail": "You do not have access to any shipments."}, status=403)        

        serializer = ShipmentBriefSerializer(shipments, many=True) 
        return Response(serializer.data)

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
        shipment = get_object_or_404(Shipment, id=id)
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)

    def patch(self, request, id): 
        shipment = get_object_or_404(Shipment, id=id)
        serializer = ShipmentSerializer(shipment, data=request.data, partial=True)

        if "address_id" in request.data: 
            try:
                address = Address.objects.get(id=request.data["address_id"])
                shipment.address = address
            except Address.DoesNotExist:
                return Response({"detail": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()        
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id): 
        shipment = get_object_or_404(Shipment, id=id)
        shipment.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)



