from .models import Admin

class AdminAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password:
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None
