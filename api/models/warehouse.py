import uuid
from django.db import models
from api.models.user import LogisticsAdministrator
from api.models.address import Address

class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="warehouses")
    logistics = models.ForeignKey(LogisticsAdministrator, on_delete=models.CASCADE, related_name="warehouses")