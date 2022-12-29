from django.contrib.auth import authenticate


from main_app.imports import *
from main_app.reset_password import get_password_token_link, validate_token
from auth_app.models import *

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, context):
        email = context["email"]
        password = context["password"]
        user = authenticate(username=context['email'], password=context['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        context = {}
        context['user']=user
        return context

class ResetPasswordEmailSerializer(serializers.Serializer):
    email_id = serializers.EmailField(max_length=65)

    class Meta:
        fields = ["email"]

    def validate(self, validated_data):
        email_id = validated_data.get("email", None)
        if not U_User.objects.filter(email=email_id).exists():
            raise ValueError("User not found")
        #send email
        return validated_data

class ResetPasswordTokenSerializer(serializers.Serializer):
    token = serializers.EmailField(max_length=300)

    class Meta:
        fields = ["token"]

    def validate(self, validated_data):
        token = validated_data.get("token", None)
        validate_token(token)
        #send email
        return validated_data