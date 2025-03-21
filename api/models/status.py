from django.utils import timezone
from django.db import models
from api.models.shipment import Shipment

class StatusType(models.TextChoices):
    CREATED = "CREATED", "Shipment Created"
    PICKED_UP = "PICKED_UP", "Picked Up"
    IN_TRANSIT = "IN_TRANSIT", "In Transit"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELED = "CANCLED", "Canceled"

class TimelineItem(models.Model): 
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="timeline",)
    status = models.CharField(max_length=30, choices=StatusType.choices, null=False, blank=False, default=StatusType.CREATED,)
    description = models.CharField(max_length=255, blank=False, null=False,)
    timestamp = models.DateTimeField(default=timezone.now,)

    class Meta:
        ordering = ["-timestamp"]