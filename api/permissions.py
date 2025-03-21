from rest_framework.permissions import BasePermission

class IsStandardUser(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_standard() 

class IsMerchant(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_merchant() 

class IsLogistics(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_logistics() 

class IsDriver(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver() 
