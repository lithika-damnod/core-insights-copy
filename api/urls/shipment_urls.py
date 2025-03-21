from django.urls import path
from api.views.shipment_view import ShipmentView

urlpatterns = [
    path('test/', ShipmentView.as_view(), name='test'),
]