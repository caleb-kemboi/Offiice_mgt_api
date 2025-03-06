from django.urls import path
from . import views

urlpatterns = [
    path('', views.delivery_list, name='delivery_list'),  # List all deliveries
    path('create/', views.create_delivery, name='create_delivery'),  # Add new delivery
    path('<int:delivery_id>/', views.delivery_detail, name='delivery_detail'),  # Delivery details
    path('edit/<delivery_id>/', views.edit_delivery, name='edit_delivery'),  # Edit delivery info
    path('<int:delivery_id>/delete/', views.delete_delivery, name='delete_delivery'),  # Delete delivery
    path('<delivery_id>/update_delivery_status/', views.update_delivery_status, name='update_delivery_status'),  # Update status
]
