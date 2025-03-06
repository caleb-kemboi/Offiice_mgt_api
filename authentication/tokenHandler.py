from django.http import JsonResponse
import jwt
from jwt import encode


from datetime import datetime, timedelta
from services.services import UserService, SessionService
from office_mgt import settings


def handle_token(user):
    try:
        # Generate JWT tokens
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

