from django.urls import path
from . import views
from .views import list_employees


urlpatterns = [
    path('create_user/', views.create_user, name='apply_for_travel'),
    path("employees/", list_employees, name="list-employees"),
    ]
