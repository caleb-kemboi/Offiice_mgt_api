import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

from services.services import UserService
from utils.models import User

def is_admin(user):
    """Check if the user is an admin."""
    return user.is_authenticated and user.is_admin()

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        supervisor_id = data.get("supervisor")

        if not username or not password or not role:
            return JsonResponse({"error": "Username, password, and role are required."}, status=400)

        if role == "employee":
            if not supervisor_id:
                return JsonResponse({"error": "Employees must have a supervisor."}, status=400)
            try:
                supervisor = User.objects.get(id=supervisor_id, role="employee")
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid supervisor ID."}, status=400)
        else:
            supervisor = None  # Non-employees don't need a supervisor

        # Create user
        user = User.objects.create_user(username=username, password=password, role=role, supervisor=supervisor)

        return JsonResponse({
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "supervisor": user.supervisor.id if user.supervisor else None
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data."}, status=400)

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
