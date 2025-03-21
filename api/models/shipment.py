import random
import string
import uuid
from datetime import datetime
from django.db import models
from api.models.user import StandardUser, MerchantAdministrator, LogisticsAdministrator
from api.models.address import Address
from api.utils.estimates import estimate_delivery_date

class Shipment(models.Model): 

    class PaymentStatus(models.TextChoices): 
        PAID = "Paid", "Paid"
        PENDING = "Pending", "Pending"
        FAILED = "Failed", "Failed"

    class PaymentMethod(models.TextChoices): 
        BANK_TRANSFER = "Bank Transfer", "Bank Transfer"
        CREDIT_CARD = "Credit Card", "Credit Card"
        OTHER = "Other", "Other"


    id = models.CharField(max_length=14, unique=True, editable=False, primary_key=True)     
    
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address")
    delivery_date = models.DateField(default=estimate_delivery_date)

    customer = models.ForeignKey(StandardUser, on_delete=models.CASCADE, related_name="customer", null=True, blank=True)
    merchant = models.ForeignKey(MerchantAdministrator, on_delete=models.CASCADE, related_name="merchant")
    logistics = models.ForeignKey(LogisticsAdministrator, on_delete=models.CASCADE, related_name="logistics")

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    package_size = models.CharField(max_length=100, null=True, blank=True)
    dimensions = models.CharField(max_length=100, null=True, blank=True)

    payment_method = models.CharField(max_length=100, choices=PaymentMethod.choices, null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=PaymentStatus.choices, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    class Meta: 
        verbose_name = "Shipment" 

    def generate_tracking_number(self):
        """Generate a unique shipping number like 'AB-432-918-2403' (YYMM at the end)"""
        prefix = ''.join(random.choices(string.ascii_uppercase, k=2))  # Random 2-letter code
        part1 = random.randint(100, 999)  # First 3-digit number
        part2 = str(uuid.uuid4().int)[-3:]  # Unique last 3 digits from UUID
        date_code = datetime.now().strftime("%y%m")  # Current year and month (YYMM)

        return f"{prefix}-{part1}-{part2}-{date_code}"

    def save(self, *args, **kwargs): 
        if not self.id: 
            new_identifier = self.generate_tracking_number()
            while Shipment.objects.filter(id=new_identifier).exists():
                new_identifier = self.generate_tracking_number()

            self.id = new_identifier
        super().save(*args, **kwargs)

    def __str__(self): 
        return f"Tracking Number: {self.id}"

