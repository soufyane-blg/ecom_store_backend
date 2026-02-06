from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "created_by") and obj.created_by == request.user