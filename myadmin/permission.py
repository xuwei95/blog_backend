from rest_framework.permissions import BasePermission
from rest_framework_jwt.utils import jwt_decode_handler
from app.models import User
class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION")[4:]
        meta = jwt_decode_handler(token)
        username = meta['username']
        user = User.objects.filter(username=username).first()
        if user.is_superuser:
            return True
        else:
            return False
