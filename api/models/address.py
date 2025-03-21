import uuid
from django.db import models
from api.models.user import User

class Address(models.Model):
    class AddressType(models.TextChoices):  
        REGULAR = "REGULAR", "Regular"
        SAVED = "SAVED", "Saved"
        PRIMARY = "PRIMARY", "Primary" 

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=AddressType.choices, default=AddressType.REGULAR)
    address_line_1 = models.CharField(max_length=255)     
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)     
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    associated_with = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="associated_with")

    def __str__(self):  
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.country}"