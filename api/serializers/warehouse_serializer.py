from rest_framework import serializers
from api.models.warehouse import Warehouse
from api.serializers.address_serializer import AddressSerializer
from api.models.address import Address
from api.models.user import LogisticsAdministrator

class WarehouseSerializer(serializers.ModelSerializer): 
    address = AddressSerializer()

    class Meta: 
        model = Warehouse
        fields = "__all__"
        read_only_fields = ['id', 'logistics']

    def create(self, validated_data):
        # Extract address data
        address_data = validated_data.pop('address')

        request = self.context.get('request')
        if request and request.user:
            address_data['associated_with'] = request.user
            validated_data["logistics"] = LogisticsAdministrator.objects.get(id = request.user.id)

        address = Address.objects.create(**address_data)

        # Create the Warehouse instance with the new address
        warehouse = Warehouse.objects.create(address=address, **validated_data)
        return warehouse