from django.urls import path
from . import views

urlpatterns = [
    path('visit_list/', views.visit_list, name='visit_list'),  # List all visits
    path('create/', views.create_visit, name='create_visit'),  # Create a new visit
    path('<int:visit_id>/', views.view_visit, name='visit_detail'),  # View visit details
    path('checkout_visitor/<visit_id>/', views.checkout_visitor, name='checkout_visitor'),  #Checkout visitor
    path('edit_visit/<visit_id>/', views.edit_visit, name='edit_visit'),  # edit_visit
    path('<int:visit_id>/delete/', views.delete_visit, name='delete_visit'),  # Delete a visit
]