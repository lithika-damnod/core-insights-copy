from django.urls import path
from api.views.addresses_view import AddressesListCreateView, AddressDetailView

urlpatterns = [
    path('', AddressesListCreateView.as_view(), name='address-create-and-list'),
    path('<uuid:address_id>/', AddressDetailView.as_view(), name='address-detail'),
]