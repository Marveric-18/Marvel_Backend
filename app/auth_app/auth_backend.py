from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from main_app.imports import *

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("YES CALLED")
        email = kwargs.get("email", None)
        print("Email", email)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None