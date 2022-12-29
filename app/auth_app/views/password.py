from auth_app.models import *
from main_app.imports import *
from main_app.reset_password import *
from auth_app.serializers import *
from rest_framework import generics

class ResetPasswordEmailRequest(APIView):
    serializer_class = ResetPasswordEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self,  request):
        try:
            pass
            return Response({"message":"User created successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordTokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        #serializer_class = ResetPasswordEmailSerializer
        # lol = get_password_token_link(U_User_Profile.objects.all().first())
        # print("lol",lol)
        try:
            return Response({"message":"User created successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, token):
        try:
            return Response({"message":"User created successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)