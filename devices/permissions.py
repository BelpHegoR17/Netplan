from rest_framework.permissions import BasePermission, SAFE_METHODS

class SunilcanEditOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_authenticated and request.user.username == 'sunil'
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        return request.user.username == 'sunil'