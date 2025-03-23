from datetime import date
from rest_framework import serializers
from api.models.shipment import Shipment
from api.models.user import MerchantAdministrator, LogisticsAdministrator
from api.models.address import Address
from django.shortcuts import get_object_or_404
from api.models.timeline import TimelineItem


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
    associated_with = serializers.SerializerMethodField()

    def get_associated_with(self, obj):
        return str(obj.customer.id) if obj.customer else None


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


class ShipmentBriefSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    merchant_name = serializers.SerializerMethodField()
    logistics_name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = Shipment
        fields = ['status', 'id', 'delivery_date', 'merchant_name', 'logistics_name', 'description']

        
    def get_status(self, obj):     
        latest_timeline_item = TimelineItem.objects.filter(shipment=obj).order_by('-shipment_sequence').first()
        if latest_timeline_item:
            return latest_timeline_item.status
        return None

    def get_merchant_name(self, obj):
        if obj.merchant:
            return obj.merchant.business_name
        return None

    def get_logistics_name(self, obj):
        if obj.logistics:
            return obj.logistics.logistics_name
        return None

    def get_description(self, obj):     
        latest_timeline_item = TimelineItem.objects.filter(shipment=obj).order_by('-shipment_sequence').first()
        if latest_timeline_item:
            return latest_timeline_item.description
        return None
