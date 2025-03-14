import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
import jwt
from django.utils.timezone import now
from jwt import encode

from datetime import datetime, timedelta

from authentication.sendOtpEmail import send_otp_email
from services.services import UserService, SessionService
from office_mgt import settings


def handle_token(user):
    try:
        access_payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'iat': datetime.utcnow()
        }
        refresh_payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow()
        }
        access_token = encode(access_payload, settings.JWT_SECRET, algorithm='HS256')
        refresh_token = encode(refresh_payload, settings.JWT_SECRET, algorithm='HS256')
        return access_token, refresh_token
    except Exception as e:
        return JsonResponse({"error": f"Error in generating token: {str(e)}"}, status=500)

def verify_jwt(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        return UserService().get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, UserService().DoesNotExist):
        return None