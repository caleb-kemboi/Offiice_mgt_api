from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from services.services import EmployeeService, VisitsService

from django.core.mail import send_mail
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from office_mgt import settings
from services.requests import get_clean_data
from django.http import JsonResponse
from django.contrib.auth import authenticate
from services.services import SessionService
from authentication.sendOtpEmail import send_otp_email
from authentication.tokenHandler import handle_token
import json
from django.contrib.auth.models import User

otp_storage = {}


@csrf_exempt
def register_user(request):
    try:
        data = get_clean_data(request)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not username or not email or not password or not first_name or not last_name:
            return JsonResponse({"error": "Missing required fields (username, email, password)"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)

        session = SessionService().filter(user=data, is_valid=True).first()

        if session:
             if session.is_otp_expired():
                session.is_valid = False
                session.save()
                session = None

             if not session:
                send_otp_email(email)  # Implement email sending
                return JsonResponse({"message": "OTP sent to your email"}, status=200, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


@csrf_exempt
def login(request):
    try:
        data = get_clean_data(request)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"message": "Username and password are required"}, status=400,safe=False)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({"message": "Invalid credentials"}, status=401, safe=False)

        # Handle session and OTP
        session = SessionService().filter(user=user, is_valid=True).first()

        if session:
            if session.is_otp_expired():
                session.is_valid = False
                session.save()
                session = None

        if not session:
            # Generate new OTP and session
            send_otp_email(user)  # Implement email sending
            return JsonResponse({"message": "OTP sent to your email"}, status=200, safe=False)

        return handle_token(user)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400,safe=False)
    except Exception as e:
        return JsonResponse({"message": f"Login error: {str(e)}"}, status=500, safe=False)


@csrf_exempt
def verify_otp(request):
    try:
        data = get_clean_data(request)
        email = data.get("email")
        otp = data.get("otp")
        password = data.get("password")
        username = data.get("username")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not email or not otp or not password or not username:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if otp_storage.get(email) == otp:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            del otp_storage[email]
            return JsonResponse({"message": "Visitor Account Created Successfully", "user_id": user.id}, status=201)
        else:
            return JsonResponse({"error": "Invalid OTP"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Missing email field"}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with this email does not exist"}, status=404)

            otp = random.randint(100000, 999999)
            otp_storage[email] = otp
            send_mail(
                "Your OTP Code for Password Reset",
                f"Your OTP code is {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({"message": "OTP sent to email. Please verify to reset password."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def verify_reset_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")
            new_password = data.get("new_password")

            if not email or not otp or not new_password:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if otp_storage.get(email) == otp:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                del otp_storage[email]
                return JsonResponse({"message": "Password reset successfully"}, status=200)
            else:
                return JsonResponse({"error": "Invalid OTP"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def notify_office_employee(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            visitor_name = data.get("visitor_name")
            visitor_email = data.get("visitor_email")
            purpose = data.get("purpose")
            employee_email = data.get("employee_email")

            if (
                not visitor_name
                or not visitor_email
                or not purpose
                or not employee_email
            ):
                return JsonResponse(
                    {"error": "Missing required fields"}, status=400
                )

            send_mail(
                "Office Visitor Notification",
                f"Visitor Name: {visitor_name}\nVisitor Email: {visitor_email}\nPurpose: {purpose}",
                settings.EMAIL_HOST_USER,
                [employee_email],
                fail_silently=False,
            )
            return JsonResponse(
                {"message": "Employee notified of visitor"}, status=200
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


####


@csrf_exempt
def register_user(request):
    try:
        data = get_clean_data(request)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not username or not email or not password or not first_name or not last_name:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if UserService().filter(email=email).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)

        hashed_password = make_password(password)
        user = UserService().create(
            username=username, email=email, password=hashed_password,
            first_name=first_name, last_name=last_name
        )

        session = SessionService().filter(user=user, is_valid=True).first()

        if session and session.is_otp_expired():
            session.is_valid = False
            session.save()
            session = None

        if not session:
            otp = send_otp_email(user)  # Implement OTP generation and email sending
            otp_storage[email] = otp  # Store OTP for verification
            return JsonResponse({"message": "OTP sent to your email"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        print("Unexpected Error:", str(e))
        return JsonResponse({"error": "Server error"}, status=500)


@csrf_exempt
def verify_register_otp(request):
    try:
        data = get_clean_data(request)
        email = data.get("email")
        otp = data.get("otp")  # Extract OTP from request

        if not email or not otp:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if otp_storage.get(email) == otp:  # Check if OTP matches
            user = UserService().create(
                email=email,
                role=data.get("role"),
                city=data.get("city"),
                address=data.get("address"),
                phone_number=data.get("phone_number"),
                date_of_birth=data.get("date_of_birth"),
                zip=data.get("zip"),  # Extract zip from request
            )

            del otp_storage[email]  # Remove OTP after successful registration

            assign_user_role(user)
            return JsonResponse({"message": "User Account Created Successfully", "user_id": user.id}, status=201)
        else:
            return JsonResponse({"error": "Invalid OTP"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)