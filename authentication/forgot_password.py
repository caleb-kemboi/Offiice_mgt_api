
"""""
from django.http import JsonResponse
from django.template.loader import render_to_string
from .sendOtpEmail import generate_otp, forgot_password_otp, send_password_changed_email
from services.requests import get_clean_data
from services.services import UserService
from utils.models import User
OTP_STORAGE = {}



def forgot_password(request):
    try:
        data = get_clean_data(request)
        username = data.get('username')

        if not username:
            return JsonResponse({"message": "Please enter Username to continue"}, status=400)

        user = UserService().get(username)  # Fetch user by username
        if not user:
            return JsonResponse({"message": "Username not found"}, status=404)

        otp = forgot_password_otp(user)  # Generate & send OTP
        OTP_STORAGE[user.email] = otp  # Store OTP temporarily

        return JsonResponse({"message": "OTP sent successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def verify_forgot_password_otp(request):
    try:
        data = get_clean_data(request)
        username = data.get('username')
        entered_otp = data.get('otp')

        if not username or not entered_otp:
            return JsonResponse({"message": "Username and OTP are required"}, status=400)

        forgot_password_user = UserService().get(username)
        if not forgot_password_user:
            return JsonResponse({"message": "Invalid username"}, status=404)

        user = forgot_password_user.email
        stored_otp = OTP_STORAGE.get(user)

        if not stored_otp:
            return JsonResponse({"message": "OTP expired or not requested"}, status=400)

        if entered_otp != stored_otp:
            return JsonResponse({"message": "Invalid OTP"}, status=400)

        return JsonResponse({"message": "OTP verified successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def reset_password(request):
    try:
        data = get_clean_data(request)
        username = data.get('username')
        new_password = data.get('new_password')

        if not username or not new_password:
            return JsonResponse({"message": "Username and new password are required"}, status=400)

        user = UserService().get(username)
        if not user:
            return JsonResponse({"message": "Invalid username"}, status=404)

        user = user.username
        user.set_password(new_password)  # Set new password securely
        user.save()

        send_password_changed_email(user)

        return JsonResponse({"message": "Password changed successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

"""