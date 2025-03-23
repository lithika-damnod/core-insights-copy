from django.urls import path
from api.views.shipment_view import ShipmentView, check_tracking_no_validity

urlpatterns = [
    path('', ShipmentView.as_view(), name='shipment_actions'),
    path('validate/', check_tracking_no_validity, name='check_tracking_no_validity'), 
]
    # path('<id>/'), # get, delete, put 
    # path('<id>/timeline'), # get, post, update, delete