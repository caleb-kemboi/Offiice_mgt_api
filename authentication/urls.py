from django.urls import path
from .tokenHandler import handle_token
from .views import login, verify_login_otp, forgot_password, verify_reset_otp, reset_password, fetch_user, logout_view, \
    refresh, resend_otp

urlpatterns = [
    path('token/', handle_token, name='handle_token'),
    path('login/', login, name='login'),
    path('verify_login_otp/', verify_login_otp, name='verify_login_otp'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_reset_otp/', verify_reset_otp, name='verify_reset_otp'),
    path('reset_password/', reset_password, name='reset_password'),
    path('user/', fetch_user, name='fetch-user'),
    path('logout/', logout_view, name='logout'),
    path('refresh/', refresh, name='refresh'),
    path('resend_otp/', resend_otp, name='resend_otp'),
]