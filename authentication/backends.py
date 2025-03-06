from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(BaseBackend):
    """
    Custom authentication backend that allows users to log in with an email and password.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # Verifies password securely
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        """Retrieve user by primary key."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None