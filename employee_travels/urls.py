from django.urls import path
from . import views

urlpatterns = [
    path('', views.travels_list, name='travels_list'),
    path('request/', views.apply_for_travel, name='apply_for_travel'),
    path('<travel_id>/', views.view_employee_travel, name='view_employee_travel'),
    path('<travel_id>/approve_travel/', views.approve_travel, name='approve_travel'),
    path('<travel_id>/decline_travel/', views.decline_travel, name='decline_travel'),
    path('<travel_id>/edit_employee_travel/', views.edit_employee_travel, name='edit_employee_travel'),

    path('<travel_id>/employee_approved_travels', views.employee_approved_travels, name='employee_approved_travels'),
    path('<travel_id>/add_expenses/', views.submit_travel_expenses, name='submit_travel_expenses'),
    path('<travel_id>/approve_expenses/', views.approve_expenses, name='approve_expenses'),
    path('<travel_id>/decline_expenses/', views.decline_expenses, name='decline_expenses'),
    path('<travel_id>/employee_approved_travels', views.employee_approved_travels, name='employee_approved_travels'),
    path('<travel_id>/employee_declined_travels', views.employee_declined_travels, name='employee_declined_travels'),
    path('<travel_id>/employee_approved_expenses', views.employee_approved_expenses, name='employee_approved_expenses'),
    path('<travel_id>/employee_declined_expenses', views.employee_declined_expenses, name='employee_declined_expenses'),

]

