from datetime import timedelta
from django.utils import timezone

# TODO: properly estimate the delivery date here...
def estimate_delivery_date():
    """
    :return: Estimated delivery date as a date object.
    """
    return timezone.now().date() + timedelta(days=5)
