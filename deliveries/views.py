import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from office_mgt import settings
from django.shortcuts import render, get_object_or_404, redirect
from services.requests import get_clean_data
from services.services import DeliveryService, UserService
from .models import Deliveries
from .utils import send_delivery_mail


@csrf_exempt
def create_delivery(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        # Extract fields correctly (ensure they are not tuples)
        item_name = data.get('item_name')
        sender_name = data.get('sender_name')
        employee_email = data.get('employee_email')
        delivery_description = data.get('delivery_description')  # Ensure this field exists in the model
        delivery_date = data.get('delivery_date')
        delivery_time = data.get('delivery_time')
        status = 'Pending Pickup'  # Default status

        # Validate required fields
        if not all([item_name, sender_name, employee_email, delivery_description, delivery_date, delivery_time]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        employee = UserService().filter(email=employee_email).first()
        # Create a new delivery record

        delivery = DeliveryService().create(
            item_name=item_name,
            sender_name=sender_name,
            employee=employee,
            delivery_description=delivery_description,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            status=status
        )

        send_delivery_mail(item_name, sender_name,employee_email, delivery_description, delivery_date)

        return JsonResponse({'message': 'Delivery created successfully', 'id': delivery.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f"Error creating delivery: {str(e)}"}, status=500)

@csrf_exempt
def update_delivery_status(request, delivery_id):
    if request.method not in ["POST", "PUT"]:
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        pickup_date = data.get('pickup_date')
        pickup_time = data.get('pickup_time')
        if not (pickup_date and pickup_time):
            return JsonResponse({"error": "Pick up date and time cant be null!"}, status=401)

        delivery = DeliveryService().get(id=delivery_id)
        if not delivery:
            return JsonResponse({"error": "Delivery not found"}, status=404)

        delivery.status = 'Delivered'
        delivery.pickup_date = pickup_date
        delivery.pickup_time = pickup_time
        delivery.save()

        return JsonResponse({"message": "Delivery Picking Updated Successfully!", "id": delivery.id}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error updating delivery: {str(e)}"}, status=500)

@csrf_exempt
def edit_delivery(request, delivery_id):
    if request.method not in ["POST", "PUT"]:
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)

        delivery = DeliveryService().get(id=delivery_id)
        if not delivery:
            return JsonResponse({"error": "Delivery not found"}, status=404)

        # Update only provided fields
        if "item_name" in data:
            delivery.item_name = data["item_name"]
        if "sender_name" in data:
            delivery.sender_name = data["sender_name"]
        if "employee_email" in data:
            delivery.employee_email = data["employee_email"]
        if "delivery_description" in data:
            delivery.delivery_description = data["delivery_description"]
        if "delivery_date" in data:
            delivery.delivery_date = data["delivery_date"]
        if "delivery_time" in data:
            delivery.delivery_time = data["delivery_time"]
        if "pickup_date" in data:
            delivery.pickup_date = data["pickup_date"]
        if "pickup_time" in data:
            delivery.pickup_time = data["pickup_time"]

        delivery.save()

        return JsonResponse({"message": "Delivery updated successfully", "id": delivery.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error updating delivery: {str(e)}"}, status=500)

@csrf_exempt
def delivery_detail(request, delivery_id):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        delivery = DeliveryService().get(id=delivery_id)
        if not delivery:
            return JsonResponse({"error": "Delivery not found"}, status=404)

        return render(request, "deliveries/delivery_detail.html", {"delivery": delivery})

    except Exception as e:
        return JsonResponse({"error": f"Error retrieving delivery: {str(e)}"}, status=500)


@csrf_exempt
def delete_delivery(request, delivery_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        delivery = DeliveryService().get(id=delivery_id)
        if not delivery:
            return JsonResponse({"error": "Delivery not found"}, status=404)

        delivery.delete()
        return JsonResponse({"message": "Delivery deleted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Error deleting delivery: {str(e)}"}, status=500)


@csrf_exempt
def delivery_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        deliveries = DeliveryService().all().order_by('-delivery_date', '-delivery_time')
        return JsonResponse({"deliveries": list(deliveries.values())}, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error retrieving deliveries: {str(e)}"}, status=500)





