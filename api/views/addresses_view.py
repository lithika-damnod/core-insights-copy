from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models.address import Address
from api.serializers.address_serializer import AddressSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

class AddressesListCreateView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        addresses = Address.objects.filter(associated_with=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def post(self, request):
        serializer = AddressSerializer(data=request.data)

        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView): 
    permission_classes=[IsAuthenticated]    

    def get(self, request, address_id):
        address = get_object_or_404(Address, id=address_id)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, address_id): 
        address = get_object_or_404(Address, id=address_id, associated_with=request.user)    
        serializer = AddressSerializer(address, data=request.data, partial=True)
        
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, address_id): 
        address = get_object_or_404(Address, id=address_id, associated_with=request.user)    
        serializer = AddressSerializer(address, data=request.data)
        
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, associated_with=request.user)
        address.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
