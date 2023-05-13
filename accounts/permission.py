from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsProfileOwnerOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        return bool(request.method == "GET" or (request.user ==  obj) or request.user.is_superuser)
