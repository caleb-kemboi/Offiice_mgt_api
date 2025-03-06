from django.urls import path
from .tokenHandler import handle_token
from .views import login, verify_login_otp,forgot_password, verify_reset_otp, reset_password

urlpatterns = [
    path('token/', handle_token, name='handle_token'),
    path('login/', login, name='login'),
    path('verify_login_otp/', verify_login_otp, name='verify_login_otp'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_reset_otp/', verify_reset_otp, name='verify_reset_otp'),
    path('reset_password/', reset_password, name='reset_password'),

]