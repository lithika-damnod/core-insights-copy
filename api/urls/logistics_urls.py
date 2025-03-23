from django.urls import path
from api.views.warehouse_view import WarehouseView, SingleWarehouseInstanceView  

urlpatterns = [
    path('warehouses/', WarehouseView.as_view(), name='warehouse_actions'),
    path('warehouses/<uuid:id>/', SingleWarehouseInstanceView.as_view(), name='single_warehouse_actions'),
]