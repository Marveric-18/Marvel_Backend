from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from datetime import datetime, timedelta, timezone
import os
import base64
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

def encode_token(user):
    secret_key = os.getenv("SECRET_KEY", "andqpQAKDLNLnlqknrmqjrqsj")

    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.now(timezone.utc) + timedelta(days=1), 
        "id": user.id
    }
    print("here")
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def get_password_token_link(user):
    token = encode_token(user)
    domain = os.getenv("MARV_BACKEND_IP", "http://127.0.0.1:3000")
    link = reverse("auth_app:reset-password-confirm", kwargs={ "token": token})
    return (domain + link).replace("reset-password", "changePassword")
    
def validate_token(token):
    try:
        secret_key = os.getenv("SECRET_KEY", "andqpQAKDLNLnlqknrmqjrqsj")
        userinfo = jwt.decode(token, secret_key)
        return userinfo
    except InvalidTokenError:
        raise ValueError("Invalid token")
    except ExpiredSignatureError:
        raise ValueError("Token Expired")