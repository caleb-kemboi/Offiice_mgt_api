from django.urls import path
from . import views

urlpatterns = [

    path('create_user/', views.create_user, name='apply_for_travel'),
    ]