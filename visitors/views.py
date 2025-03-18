
from services.services import UserService, VisitsService
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from visitors.utils import send_host_email, send_employee_email


@csrf_exempt
def create_visit(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    try:
        data = json.loads(request.body)
        visitor_first_name = data.get('visitor_first_name')
        visitor_last_name = data.get('visitor_last_name')
        visitor_phone = data.get('visitor_phone')
        visitor_email = data.get('visitor_email')
        visit_purpose =data.get('visit_purpose')
        visit_date = data.get('visit_date')
        visit_time = data.get('visit_time')
        employee_email = data.get('employee_email')

        if not (visitor_first_name and visitor_last_name and visitor_phone and visit_purpose and employee_email
                and visitor_email and visit_date):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Check if the visitor already exists, otherwise create a new one

        employee = UserService().filter(email=employee_email).first()

        employee_busy = VisitsService().filter(
            employee=employee,
            visit_date=visit_date,
            visit_time=visit_time
        ).exists()

        if employee_busy:
            return JsonResponse({'error': 'Employee is not available at this time. Please select another slot.'},
                                status=400)

        try:

          visit = VisitsService().create(
                    employee=employee,
                    visit_purpose = visit_purpose,
                    visit_date = visit_date,
                  visitor_first_name = visitor_first_name,
                  visitor_last_name = visitor_last_name,
                  visitor_phone = visitor_phone,
                  visitor_email = visitor_email,
                  visit_time = visit_time
                )
          send_host_email(employee_email, visitor_first_name, visitor_last_name,
                          visit_purpose, visit_date)
          send_employee_email(visitor_email,
                              visit_purpose, visit_date, employee)
          return JsonResponse({"message": "Visit Created Successfully", "id": visit.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": f"Error creating visit: {str(e)}"}, status=500)


    except Exception as e:
        return JsonResponse({"error": f"Error updating visit: {str(e)}"}, status=500)


@csrf_exempt
def checkout_visitor(request, visit_id):

    if request.method not in ["POST", "PUT"]:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    data = json.loads(request.body)
    checkout_time = data.get('checkout_time')

    try:
        visit = VisitsService().get(id=visit_id)
        if not visit:
            return JsonResponse({"error": "Visit not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error retrieving visit: {str(e)}"}, status=500)
    try:
           visit.checkout_time = checkout_time
           visit.save()
           return JsonResponse({"message": "Visitor Checked out successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error updating visit: {str(e)}"}, status=500)

@csrf_exempt
def edit_visit(request, visit_id):
    try:
        visit = VisitsService().get(id=visit_id)
        if not visit:
            return JsonResponse({"error": "Visit not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error retrieving visit: {str(e)}"}, status=500)

    if request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            # Only update fields if they exist in request data
            visit.visitor_first_name = data.get('visitor_first_name', visit.visitor_first_name)
            visit.visitor_last_name = data.get('visitor_last_name', visit.visitor_last_name)
            visit.visitor_email = data.get('visitor_email', visit.visitor_email)
            visit.visit_purpose = data.get('visit_purpose', visit.visit_purpose)
            visit.visit_date = data.get('visit_date', visit.visit_date)
            visit.visit_time = data.get('visit_time', visit.visit_time)
            visit.visitor_phone = data.get('visitor_phone', visit.visitor_phone)

            visit.save()
            return JsonResponse({"message": "Visit updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error updating visit: {str(e)}"}, status=500)

    return render(request, 'visits/edit_visit.html', {'visit': visit})


@csrf_exempt
def visit_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    visits = VisitsService().all().order_by('-date', '-time')  # Ensure it returns a QuerySet

    return render(request, 'visits/visit_list.html', {'visits': visits})

@csrf_exempt
def view_visit(request, visit_id):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        visit = VisitsService().get(id=visit_id)
        if not visit:
            return JsonResponse({"error": "Visit not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error retrieving visit: {str(e)}"}, status=500)

    return render(request, 'visits/view_visit.html', {'visit': visit})


@csrf_exempt
def delete_visit(request, visit_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        visit = VisitsService().get(id=visit_id)
        if not visit:
            return JsonResponse({"error": "Visit not found"}, status=404)

        visit.delete()
        return JsonResponse({"message": "Visit deleted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Error deleting visit: {str(e)}"}, status=500)


