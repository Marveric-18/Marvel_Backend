from main_app.imports import *
from auth_app.models import *

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = U_User
        fields = (
            'recovery_email',
            'is_active',
            'two_way_auth'
        )

    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        print(validated_data)
        email = validated_data.get("email", None)
        password = validated_data.pop("password", None)
        
        if not email or not password:
            raise ValueError("Please enter valid email and password")
        email = validate_email(email)
        if U_User.objects.filter(Q(email__iexact=email)).distinct():
            raise ValueError("User already exists with entered email")
        if U_User_Profile.objects.filter(Q(email__iexact=email)).distinct():
            raise ValueError("User already exists with entered email")
        user =  U_User.objects.create_user(
                    email=email,
                    username=email,
                    password=password,
                    recovery_email = validated_data.pop("recovery_email", email),
                )
        validated_data['user'] = user
        try:
            profile = UserProfile_Serializer(data=validated_data)
            if profile.is_valid():
                profile.save()
                return user
            raise ValueError("User profile can not be created")
        except:
            user =  U_User.objects.delete(email = email)
            raise ValueError("User profile can not be created")
        

class UserProfile_Serializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(source='get_token', read_only=True)
    user_info = serializers.SerializerMethodField()
    def get_token(self, profile):
        token = {}
        token = get_tokens_for_user(profile)
        return token

    def get_user_info(self, profile):
        if not profile.is_social:
            return  User_Serializer(U_User.objects.get(email= profile.email)).data
        return {}

    def to_internal_value(self, data):
        return data


    class Meta:
        model = U_User_Profile
        fields = (
            'email',
            'username',
            'profile_img',
            'token',
            'first_name',
            'last_name',
            'phone',
            'bio',
            'weblink',
            'is_active',
            'is_social',
            'token',
            'user_info',
        )
    
    def create(self, validated_data):
        email = validated_data.get("email", None)
        first_name = validated_data.get("first_name", None)
        last_name = validated_data.get("last_name", None)
        user  = validated_data.get("user", None)
        print("user", user)
        try:
            profile = U_User_Profile.objects.create(
                email = email,
                first_name = first_name,
                last_name = last_name,
                user = user
            )
            return profile
        except:
            raise ValueError("User profile can not be created")