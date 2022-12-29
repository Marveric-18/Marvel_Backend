from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.decorators import action, permission_classes
from rest_framework import views, permissions
from rest_framework.views import APIView
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


from main_app.custom_func import validate_email