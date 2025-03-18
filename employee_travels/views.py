from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from employee_travels.utils import get_supervisor_email, send_travel_request_mail, send_approve_mail, send_decline_mail, \
    send_travel_expenses_mail
from services.requests import get_clean_data
from django.http import JsonResponse
from services.services import SessionService, EmployeeTravelService, UserService
import json


@csrf_exempt
def apply_for_travel(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=405)

        data = json.loads(request.body)

        travel_title = data.get("travel_title")
        travel_purpose = data.get("travel_purpose")
        employee_email = data.get("employee_email")
        travel_applied_on = data.get("travel_applied_on")
        travel_date_from = data.get("travel_date_from")
        travel_date_to = data.get("travel_date_to")
        travel_destination = data.get("travel_destination")
        mode_of_transport = data.get("mode_of_transport")
        travel_budget = data.get("travel_budget")
        travel_approval_status = 'Pending Supervisor Approval'

        required_fields = [
            "travel_title", "travel_purpose", "employee_email", "travel_date_from", "travel_date_to",
            "travel_destination", "mode_of_transport", "travel_budget"
        ]

        # Ensure all required fields are present
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

        # Get the employee object
        employee = UserService().get(email=employee_email)
        if not employee:
            return JsonResponse({"error": "Employee not found"}, status=404)

        # Ensure the requester is not an admin (Admins don’t have supervisors)
        if employee.is_admin():
            return JsonResponse({"error": "Admins cannot apply for travel"}, status=403)

        # Get the supervisor email
        if employee.supervisor:
            supervisor_email = employee.supervisor.email
        else:
            return JsonResponse({"error": "Supervisor not assigned"}, status=400)

        # Create the travel request
        travel_request = EmployeeTravelService().create(
            travel_title=travel_title,
            travel_purpose=travel_purpose,
            employee=employee,
            travel_date_from=travel_date_from,
            travel_date_to=travel_date_to,
            travel_destination=travel_destination,
            mode_of_transport=mode_of_transport,
            travel_budget=travel_budget,
            travel_approval_status=travel_approval_status,
            travel_applied_on=travel_applied_on
        )

        # Send email to the supervisor
        send_travel_request_mail(supervisor_email, travel_title, employee, travel_applied_on, travel_purpose)

        return JsonResponse({"message": "Travel request submitted", "id": travel_request.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def approve_travel(request, travel_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)


    try:
        update_travel = EmployeeTravelService().get(id=travel_id)

        if not update_travel:
            return JsonResponse({"error": "Travel request not found"}, status=404)

        data = json.loads(request.body)
        supervisor_note = data.get("supervisor_note")

        new_travel_status = 'Approved'
        update_travel.supervisor_note = supervisor_note
        update_travel.travel_approval_status = new_travel_status
        travel_title = update_travel.travel_title
        employee = update_travel.employee
        travel_applied_on = update_travel.travel_applied_on
        travel_purpose = update_travel.travel_purpose

        update_travel.save()
        send_approve_mail(travel_title, employee, travel_applied_on, travel_purpose)

        return JsonResponse(
            {"message": f"Travel application has been Approved and the employee notified"},
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def decline_travel(request, travel_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        update_travel = EmployeeTravelService().get(id=travel_id)

        if not update_travel:
            return JsonResponse({"error": "Travel request not found"}, status=404)

        data = json.loads(request.body)
        supervisor_note = data.get("supervisor_note")
        if not supervisor_note:
            return JsonResponse({"error": "Please provide reason for decline."})

        new_travel_status = 'Declined'
        update_travel.travel_approval_status = new_travel_status
        travel_title = update_travel.travel_title
        employee = update_travel.employee
        travel_applied_on = update_travel.travel_applied_on
        travel_purpose = update_travel.travel_purpose
        update_travel.save()
        send_decline_mail(travel_title, employee, travel_applied_on, travel_purpose, supervisor_note)
        # Determine message based on status
        #decision_message = "Approved" if new_travel_status == "Approved" else "Declined"

        # TODO: Add email notification logic here

        return JsonResponse(
            {"message": f"Travel application has been Declined and the employee notified"},
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def travels_list(request):
    travels = EmployeeTravelService().all()
    return render(request, "employee_travels_list.html", {"travels": travels})


@csrf_exempt
def view_employee_travel(request, travel_id):
    travel_entry = EmployeeTravelService().get(id=travel_id)

    if not travel_entry:
        return JsonResponse({"error": "Travel entry not found"}, status=404)

    return render(request, 'employee_travel/view_travel.html', {'travel_entry': travel_entry})

@csrf_exempt
def edit_employee_travel(request, travel_id):
    try:
        # Get the travel entry from the database
        travel_entry = EmployeeTravelService().filter(id=travel_id).first()
        if not travel_entry:
            return JsonResponse({"error": "Travel entry not found"}, status=404)

        # Parse JSON data from request
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # List of fields to update
        fields_to_update = [
            "travel_title", "travel_purpose", "travel_applied_on",
            "travel_date_from", "travel_date_to", "travel_destination",
            "mode_of_transport", "travel_budget", "date_expenses_submitted",
            "travel_expenses_amount", "expenses_description"
        ]

        # Update fields dynamically
        for field in fields_to_update:
            if field in data:
                setattr(travel_entry, field, data[field])

        # Handle employee field separately (convert email to Employee instance)
        if "employee" in data:
            employee_email = data["employee"]
            employee_instance = EmployeeService().filter(employee_email=employee_email).first()
            if not employee_instance:
                return JsonResponse({"error": "Employee not found"}, status=404)
            travel_entry.employee = employee_instance  # Assign the Employee instance

        # Save updated travel entry
        travel_entry.save()

        return JsonResponse({"message": "Travel request updated successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Something went wrong: {str(e)}"}, status=500)

@csrf_exempt
def submit_travel_expenses(request, travel_id):
    if request.method != "POST" and "PUT":
        return JsonResponse({"error": "Invalid request method"}, status=405)



    try:
        data = get_clean_data(request)  # Assuming this properly sanitizes input


        travel_for_expense = EmployeeTravelService().get(id=travel_id)

        required_fields = ["travel_expenses_amount", "expenses_description", "expenses_date_submitted"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

        data = json.loads(request.body)
        travel_for_expense.travel_expenses_amount = data.get("travel_expenses_amount")
        travel_for_expense.expenses_description = data.get("expenses_description")
        #new_travel_status = "Pending Approval"
        travel_for_expense.expenses_approval_Status = 'Pending Approval'
        travel_title = travel_for_expense.travel_title
        travel_applied_on = travel_for_expense.travel_applied_on
        travel_purpose = travel_for_expense.travel_purpose

        employee = travel_for_expense.employee
        supervisor_email = get_supervisor_email(employee)
        send_travel_expenses_mail(supervisor_email, travel_title, employee, travel_applied_on, travel_for_expense.expenses_description, travel_for_expense.travel_expenses_amount)
        travel_for_expense.save()

        return JsonResponse(
            {'message': 'Travel Expenses submitted successfully'},
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def approve_expenses(request, travel_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        update_expenses = EmployeeTravelService().get(id=travel_id)

        if not update_expenses:
            return JsonResponse({"error": "Expense record not found"}, status=404)

        new_expense_status = 'Approved'
        update_expenses.expenses_approval_Status = new_expense_status

        update_expenses.save()


        # TODO: Add email notification logic here

        return JsonResponse(
            {"message": f"Travel expenses have been Approved and the employee notified"},
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def decline_expenses(request, travel_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        update_expenses = EmployeeTravelService().get(id=travel_id)

        if not update_expenses:
            return JsonResponse({"error": "Expense record not found"}, status=404)

        new_expense_status = 'Declined'
        update_expenses.expenses_approval_Status = new_expense_status
        update_expenses.save()

        # TODO: Add email notification logic here

        return JsonResponse(
            {"message": f"Travel expenses have been Declined and the employee notified"},
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def employee_approved_travels(request, user_id):

    travels = EmployeeTravelService().filter(id=user_id, travel_approval_status='Approved')

    return render(request, "employee_travels_list.html", {"travels": travels})


@csrf_exempt
def employee_declined_travels(request, user_id):
    travels = EmployeeTravelService().filter(id=user_id, travel_approval_status='Declined')

    return render(request, "employee_travels_list.html", {"travels": travels})


@csrf_exempt
def employee_approved_expenses(request, user_id):
    travels = EmployeeTravelService().filter(id=user_id, expenses_approval_Status='Approved')

    return render(request, "employee_travels_list.html", {"travels": travels})


@csrf_exempt
def employee_declined_expenses(request, user_id):
    travels = EmployeeTravelService().filter(id=user_id, expenses_approval_Status='Declined')

    return render(request, "employee_travels_list.html", {"travels": travels})

