from django.urls import path
from . import views
from .views import list_employees, employee_dropdown, employee_update, employee_delete

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path("employees/", list_employees, name="list-employees"),
    path("employee_dropdown/", employee_dropdown, name="employee_dropdown"),
    path("employee_update/<int:id>/", employee_update, name="employee_update"),
    path("employee_delete/<int:id>/", employee_delete, name="employee_delete"),

]
