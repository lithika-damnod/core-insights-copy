from rest_framework import serializers
from api.models import TimelineItem, Shipment

class TimelineItemSerializer(serializers.ModelSerializer):
    shipment_id = serializers.UUIDField(source="shipment.id", read_only=True)
    shipment_sequence = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TimelineItem
        fields = [
            "shipment_id",
            "shipment_sequence",
            "status",
            "description",
            "timestamp",
            "latitude",
            "longitude",
        ]
