from django.urls import path
from api.views.shipment_view import ShipmentView, ShipmentById, check_tracking_no_validity, link_shipment
from api.views.timeline_view import TimelineView, deleteTimeLineItemByKey

urlpatterns = [
    path('', ShipmentView.as_view(), name='shipment_actions'),
    path('validate/', check_tracking_no_validity, name='check_tracking_no_validity'), 
    path('<str:id>/', ShipmentById.as_view(), name='shipment_by_id'),
    path('<str:id>/link/', link_shipment, name='link_shipment'),
    path('<str:id>/timeline/', TimelineView.as_view(), name='timeline'),
    path('<str:id>/timeline/<str:key>/', deleteTimeLineItemByKey, name='delete_timeline_item')
]