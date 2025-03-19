import random
import string
from datetime import timedelta

from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.cache import cache
from django.utils.timezone import now

from services.services import SessionService, UserService
from office_mgt import settings


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))


def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user,otp):
  try:
    SessionService().create(
        user=user,
        otp=otp,
        is_valid=True
    )

    html_content = render_to_string('otp_email_template.html', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="Your OTP Code",
            body=f"Your OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return user

  except Exception as e:
        print(f"Error sending OTP email: {e}")

"""""
def forgot_password_otp(user):
    #otp = generate_otp()

    try:
        html_content = render_to_string('forgot_password_otp.html', {'otp': otp})
        email = EmailMultiAlternatives(
            subject="Your OTP Code",
            body=f"Your OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Error sending OTP email: {e}")

    return otp
"""
def send_password_changed_email(user):
    try:
        html_content = render_to_string('password_changed.html', {'user': user})
        email = EmailMultiAlternatives(
            subject="Password Changed Successfully",
            body="Your password has been changed successfully. If this was not you, please contact support immediately.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Error sending password change email: {e}")

def send_new_user_details(user, password):
    try:
        #html_content = render_to_string('password_changed.html', {'user': user})
        email = EmailMultiAlternatives(
            subject="Account Created Successfully",
            body=f"Your account has been changed successfully. Your new password: {password}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
       #email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Error sending password change email: {e}")


