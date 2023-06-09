from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == "1")

class IsPatientsDoctor(BasePermission): #Medical staff can GET only info, if doctor worked on patient can touch data.
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == "1")

    def has_object_permission(self, request, view, obj):
        return bool(request.method == "GET" or request.user in obj.doctor.all())


class IsDoctorForFile(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == "1")
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user in obj.patient_history.doctor.all())


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))