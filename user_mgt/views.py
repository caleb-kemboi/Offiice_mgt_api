import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

from services.services import UserService
from utils.models import User

def is_admin(user):
    """Check if the user is an admin."""
    return user.is_authenticated and user.is_admin()

@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)

        # Validate required fields
        required_fields = ["username", "password", "first_name", "last_name", "role"]
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({"error": f"{field} is required."}, status=400)

        # Check if the role is valid
        valid_roles = ["admin", "employee", "receptionist"]
        if data["role"] not in valid_roles:
            return JsonResponse({"error": "Invalid role."}, status=400)

        # Validate supervisor if the role is an employee
        supervisor = None
        if data["role"] == "employee" and "supervisor_id" in data:
            try:
                supervisor = User.objects.get(id=data["supervisor_id"])
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid supervisor ID."}, status=400)

        # Create the user
        user = User.objects.create_user(
            email=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role=data["role"],
            supervisor=supervisor
        )
        return JsonResponse({"message": "User created successfully!", "user_id": user.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def list_employees(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Fetch all employees
        employees = User.objects.all().values(
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "supervisor__email"
        )

        # Count total employees
        total_employees = User.objects.count()

        # Count by roles
        total_admins = UserService().filter(role="admin").count()
        total_receptionists = UserService().filter(role="receptionist").count()
        total_supervisors = UserService().filter(
            role="employee", supervised_employees__isnull=False
        ).distinct().count()
        total_regular_employees = UserService().filter(role="employee").count()

        # Format the response
        return JsonResponse({
            "total_employees": total_employees,
            "total_admins": total_admins,
            "total_receptionists": total_receptionists,
            "total_supervisors": total_supervisors,
            "total_regular_employees": total_regular_employees,
            "employees": list(employees)
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def employee_dropdown(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Fetch all users for the Supervisor dropdown
        employees = User.objects.all().values(
            "id", "first_name", "last_name", "email", "phone_number", "role", "supervisor__email"
        )

        # Count total users and by role
        total_employees = User.objects.count()
        total_admins = User.objects.filter(role="admin").count()
        total_receptionists = User.objects.filter(role="receptionist").count()
        total_supervisors = User.objects.filter(role="employee", supervised_employees__isnull=False).distinct().count()
        total_regular_employees = User.objects.filter(role="employee").count()

        return JsonResponse({
            "total_employees": total_employees,
            "total_admins": total_admins,
            "total_receptionists": total_receptionists,
            "total_supervisors": total_supervisors,
            "total_regular_employees": total_regular_employees,
            "employees": list(employees)
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




@csrf_exempt  # Disable CSRF for simplicity (use with caution in production)
def employee_update(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            employee = User.objects.get(id=id)
            employee.first_name = data.get('first_name', employee.first_name)
            employee.last_name = data.get('last_name', employee.last_name)
            employee.email = data.get('email', employee.email)
            employee.phone_number = data.get('phone_number', employee.phone_number)
            employee.role = data.get('role', employee.role)

            supervisor_id = data.get('supervisor')
            if supervisor_id is not None:
                try:
                    employee.supervisor = User.objects.get(id=supervisor_id)
                except User.DoesNotExist:
                    employee.supervisor = None
            else:
                employee.supervisor = None

            employee.save()

            response_data = {
                'id': employee.id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email,
                'phone_number': employee.phone_number,
                'role': employee.role,
                'supervisor': employee.supervisor.id if employee.supervisor else None,
            }

            return JsonResponse(response_data, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return HttpResponse(status=405)

@csrf_exempt
def employee_delete(request, id):
    print(f"Received DELETE request for user ID: {id}")
    if request.method == 'DELETE':
        try:
            print(f"Attempting to fetch user with ID: {id}")
            user = User.objects.get(id=id)  # Use your custom User model
            print(f"Found user: {user.email} (Role: {user.role})")
            # Optional: Restrict to "employee" role
            if user.role not in ['employee', 'receptionist']:
                print(f"User {id} is not an employee/receptionist: {user.role}")
                return JsonResponse({'error': 'User is not an employee'}, status=403)
            user.delete()
            print(f"User {id} deleted successfully")
            return JsonResponse({'message': 'Employee deleted successfully'}, status=200)
        except User.DoesNotExist:
            print(f"User with ID {id} not found")
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            error_msg = str(e)
            print(f"Error deleting user {id}: {error_msg}")
            return JsonResponse({'error': f'Failed to delete: {error_msg}'}, status=500)
    else:
        print(f"Invalid method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'}, status=405)