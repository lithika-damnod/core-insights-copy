from django.utils import timezone
from django.db import models
from api.models.shipment import Shipment

class TimelineItem(models.Model): 
    class StatusType(models.TextChoices):
        CREATED = "CREATED", "Shipment Created"
        PICKED_UP = "PICKED_UP", "Picked Up"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELED = "CANCLED", "Canceled"

    shipment_sequence = models.PositiveIntegerField(editable=False, null=True, blank=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="timeline",)
    status = models.CharField(max_length=30, choices=StatusType.choices, null=False, blank=False, default=StatusType.CREATED,)
    description = models.CharField(max_length=255, blank=False, null=False,)
    timestamp = models.DateTimeField(default=timezone.now,)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    class Meta:
        ordering = ["-timestamp"]

    def save(self, *args, **kwargs):
        if not self.pk:
            last_item = TimelineItem.objects.filter(shipment=self.shipment).order_by("-shipment_sequence").first()
            self.shipment_sequence = (last_item.shipment_sequence + 1) if last_item else 1
        super().save(*args, **kwargs)

    def __str__(self): 
        return f"{self.shipment.id} ({self.shipment_sequence})"
