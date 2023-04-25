from django.contrib.auth import authenticate, login

from auth_app.models import *
from main_app.imports import *
from auth_app.serializers import *

from .verify_token import verify_token
from main_app.custom_func import upload_image_to_user_path

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login_request(request):
    if request.method=="POST":
        try:
            print(request.data)
            email_or_username = request.data.get("email", None)
            queryset = U_User.objects.filter(
                Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)
            )
            if not queryset.first():
                return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
            
            password = request.data.get("password", None)
            if not queryset.distinct():
                return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            username = queryset[0].username
            user = authenticate(request, username=username, password=password)
            if user is None:
                return Response({"message":"Please enter correct password"},status=status.HTTP_401_UNAUTHORIZED)
            try:
                login(request, user)
                profile_obj = U_User_Profile.objects.get(email= user.email)
                serializer = UserProfile_Serializer(profile_obj)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Exception: {e}")
                return Response({"message":"Authentication error"},status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message":"Forbidden method"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login_social(request):
    try:
        backend = request.data.get("backend", None)
        token = request.data.get("token", None)
        full_name = request.data.get("full_name", None)
        profile_image = request.data.get("profile_image", None)
        email_or_username = request.data.get("email", None)
        queryset = U_User.objects.filter(
            Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)
        )
        if queryset.first():
            return Response({"message":"You already have an account. Please login with username and password"},status=status.HTTP_404_NOT_FOUND)
        if not backend or not token:
            return Response({"message":"Please provide token and backend"},status=status.HTTP_403_FORBIDDEN)
        try:
            verify_token(token, backend)
        except:
            return Response({"message":"Invalid access token"},status=status.HTTP_403_FORBIDDEN)
        queryset = U_User_Profile.objects.filter(
            Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)
        )
        first_name = None
        last_name = None
        if full_name:
            full_name = full_name.split(" ")
            if len(full_name) == 2:
                first_name = full_name[0]
                last_name = full_name[0]
        if not queryset.s():
            profile = U_User_Profile.objects.create(
                email = email_or_username,
                first_name = first_name,
                last_name = last_name,
                is_social = True,
            )
            if profile_image:
                try:
                    profile.profile_img = upload_image_to_user_path(profile, profile_image)
                    profile.save()
                except:
                    pass
            queryset = U_User_Profile.objects.filter(
                Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)
            )
        serializer = UserProfile_Serializer(queryset.first()) 
        return Response(serializer.data,status=status.HTTP_200_OK)   
    except:
        return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)