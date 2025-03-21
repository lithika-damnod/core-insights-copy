from datetime import date
from rest_framework import serializers
from api.models.shipment import Shipment
from api.models.user import MerchantAdministrator, LogisticsAdministrator
from api.models.address import Address
from django.shortcuts import get_object_or_404


class AddressSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Address
        fields = "__all__"
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("associated_with", None)
        return data

class MerchantAdministratorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='business_name')
    associated_with = serializers.UUIDField(source='id')

    class Meta: 
        model = MerchantAdministrator
        fields = ['name', 'associated_with']

class LogisticsAdministratorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='logistics_name')
    associated_with = serializers.UUIDField(source='id')

    class Meta: 
        model = LogisticsAdministrator
        fields = ['name', 'associated_with']

class RecipientSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    telephone = serializers.CharField()
    address = AddressSerializer()
    associated_with = serializers.UUIDField(source="customer")

class PackageSerializer(serializers.Serializer):
    weight = serializers.DecimalField(max_digits=6, decimal_places=2)
    package_size = serializers.CharField()
    dimensions = serializers.CharField()

class PaymentSerializer(serializers.Serializer):
    payment_method = serializers.CharField() 
    payment_status = serializers.CharField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2) 


class ShipmentSerializer(serializers.ModelSerializer): 
    address = AddressSerializer(write_only=True) 
    
    recipient =  serializers.SerializerMethodField()
    merchant = serializers.UUIDField(write_only=True)
    merchant = MerchantAdministratorSerializer(read_only=True)

    logistics_id = serializers.UUIDField(write_only=True)
    logistics = LogisticsAdministratorSerializer(read_only=True)

    package = serializers.SerializerMethodField() 
    payment = serializers.SerializerMethodField() 

    
    class Meta: 
        model = Shipment
        fields = "__all__"   
        read_only_fields = ['id', 'merchant', 'delivery_date']
        extra_kwargs = {field: {"write_only": True} for field in (
            "customer", "first_name", "last_name", "telephone",
            "weight", "package_size", "dimensions",
            "payment_method", "payment_status", "total_cost"
        )}

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        # address_instance, _ = Address.objects.get_or_create(**address_data)
        address_instance = Address.objects.create(**address_data)

        logistics_id = validated_data.pop("logistics_id")
        logistics_instance = get_object_or_404(LogisticsAdministrator, id=logistics_id) 

        # Create the Shipment with the associated address
        shipment = Shipment.objects.create(address=address_instance, logistics=logistics_instance, **validated_data)
        return shipment

    def get_recipient(self, instance):
        return RecipientSerializer(instance).data

    def get_package(self, instance):
        return PackageSerializer(instance).data

    def get_payment(self, instance):
        return PaymentSerializer(instance).data

