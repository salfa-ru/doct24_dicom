from rest_framework.permissions import BasePermission
from auth_app.models import User


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )
