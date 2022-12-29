from os import name
from django.contrib import admin
from django.urls import path, include

from .views import *

app_name = "auth_app"

urlpatterns = [
    path('login', login_request, name="login"),
    path('login/social', login_social, name="login-social"),
    path('signup', CreateUserView.as_view(), name="signup"),

    path('reset-password', ResetPasswordView.as_view(), name="reset-password"),
    path('reset-password/<token>', ResetPasswordView.as_view(), name="reset-password-confirm")
]