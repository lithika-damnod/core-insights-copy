from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsLogistics
from api.serializers.warehouse_serializer import WarehouseSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models.warehouse import Warehouse
from api.models.user import LogisticsAdministrator

class WarehouseView(APIView): 
    permission_classes = [IsLogistics]
    
    def get(self, request): 
        user = LogisticsAdministrator.objects.get(id=request.user.id)
        warehouses = Warehouse.objects.filter(logistics=user)
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)
    
    def post(self, request): 
        serializer = WarehouseSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleWarehouseInstanceView(APIView): 
    permission_classes = [IsLogistics]

    def get(self, request, id): 
        shipment = get_object_or_404(Warehouse, id=id)
        serializer = WarehouseSerializer(shipment)
        return Response(serializer.data)

    def delete(self, request, id): 
        shipment = get_object_or_404(Warehouse, id=id)
        shipment.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)