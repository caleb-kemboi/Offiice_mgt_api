from datetime import timedelta
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from authentication.sendOtpEmail import send_otp_email
from authentication.tokenHandler import handle_token
from services.services import SessionService, UserService
import json
import re
from django.contrib.auth.hashers import make_password




@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        otp = user.generate_otp()
        user.otp = otp
        user.otp_expiry = now() + timedelta(minutes=5)
        user.save()
        send_otp_email(user, otp)

        return JsonResponse({"message": "OTP sent successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({"message": f"Login error: {str(e)}"}, status=500, safe=False)

@csrf_exempt
def verify_login_otp(request):
    """Step 2: User submits OTP to complete login."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")

            if not email or not otp:
                return JsonResponse({"message": "Email and OTP are required"}, status=400)

            user = UserService().filter(email=email).first()
            if not user or user.otp != otp or now() > user.otp_expiry:
                return JsonResponse({"error": "Invalid or expired OTP"}, status=401)

            user.otp = None  # Clear OTP after verification
            user.otp_expiry = None
            user.is_otp_verified = True
            user.save()

            access_token, refresh_token = handle_token(user)

            response = JsonResponse({"message": "OTP verified, login successful"})
            #Return Homepage
            response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax", max_age=900)
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Lax",
                                max_age=604800)

            return response
        except Exception as e:
         return JsonResponse({"error": f"OTP verification error: {str(e)}"}, status=500)

@csrf_exempt
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({"message": "Please enter Email to continue"}, status=400)

            # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({"message": "Invalid email format"}, status=400)

        user = UserService().filter(email=email).first()
        if not user:
            return JsonResponse({"message": "Username not found, Please enter Valid Email to continue"}, status=404)

        reset_otp = user.generate_otp()
        user.reset_otp = reset_otp
        user.reset_otp_expiry = now() + timedelta(minutes=5)
        user.save()
        send_otp_email(user, reset_otp)

        return JsonResponse({"message": "Reset Password OTP sent successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({"message": f"Reset Password error: {str(e)}"}, status=500, safe=False)


@csrf_exempt
def verify_reset_otp(request):
    """Step 2: User submits OTP to complete login."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            reset_otp = data.get("otp")

            if not email or not reset_otp:
                return JsonResponse({"message": "Email and OTP are required"}, status=400)

            user = UserService().filter(email=email).first()
            if not user or user.reset_otp != reset_otp or now() > user.reset_otp_expiry:
                return JsonResponse({"error": "Invalid or expired OTP"}, status=401)

            user.reset_otp = None  # Clear OTP after verification
            user.is_reset_otp_verified = True
            user.save()

            access_token, refresh_token = handle_token(user)

            response = JsonResponse({"message": "Reset OTP verified"})
            response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Lax", max_age=900)
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Lax",
                                max_age=604800)

            return response
        except Exception as e:
         return JsonResponse({"error": f"OTP verification error: {str(e)}"}, status=500)



@csrf_exempt
def reset_password(request):
    """Step 3: Reset user password after OTP verification."""

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            new_password = data.get("new_password")

            if not email or not new_password:
                return JsonResponse({"message": "Email and new password are required"}, status=400)

            user = UserService().filter(email=email).first()
            if not user:
                return JsonResponse({"message": "User not found"}, status=404)

            # Ensure OTP verification status before allowing password reset
            if not user.is_reset_otp_verified:
                return JsonResponse({"message": "OTP verification is required before resetting the password"}, status=403)

            # Validate password strength
            if len(new_password) < 8 or not re.search(r"[A-Za-z]", new_password) or not re.search(r"\d", new_password):
                return JsonResponse({"message": "Password must be at least 8 characters long and include letters and numbers"}, status=400)

            # Securely hash the password before saving
            user.password = make_password(new_password)

            # Clear OTP-related fields securely
            user.is_reset_otp_verified = False  # Reset verification flag
            user.reset_otp = None
            user.reset_otp_expiry = None
            user.save()

            return JsonResponse({"message": "Password reset successfully. You can now log in."})

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Password reset error: {str(e)}"}, status=500)

