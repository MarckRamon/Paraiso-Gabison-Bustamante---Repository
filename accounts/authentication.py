from django.contrib.auth.hashers import check_password
from .models import Admin

class AdminAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            admin = Admin.objects.get(username=username)
            if check_password(password, admin.password):  # Use check_password to compare hashed passwords
                return admin
            return None
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None