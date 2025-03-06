from django.core.mail import EmailMultiAlternatives

from office_mgt import settings


def send_travel_request_mail(supervisor_email, travel_title, employee, travel_applied_on, travel_purpose):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="Your Have Received a Travel  Request Pending Approval",
            body=f"Your have a travel request: {travel_title}  from {employee.employee_first_name} {employee.employee_second_name} on {travel_applied_on} "
                 f"Travel details: {travel_purpose}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[supervisor_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return travel_title
  except Exception as e:
        print(f"Error sending OTP email: {e}")

def get_supervisor_email(employee):
            if employee.supervisor:
                return employee.supervisor.employee_email
            return None

def send_approve_mail(travel_title, employee, travel_applied_on, travel_purpose):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="TRAVEL REQUEST APPROVAL",
            body=f"Your travel request: {travel_title}  from {employee.employee_first_name} {employee.employee_second_name} applied on {travel_applied_on}  "
                 f"has been APPROVED!"
                 f"Travel details: {travel_purpose}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee.employee_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return travel_title
  except Exception as e:
        print(f"Error sending OTP email: {e}")

def send_decline_mail(travel_title, employee, travel_applied_on, travel_purpose, supervisor_note):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="TRAVEL REQUEST DECLINED",
            body=f"Your travel request: {travel_title}  from {employee.employee_first_name} {employee.employee_second_name} applied on {travel_applied_on}  "
                 f"has been Declined!"
                 f"Travel details: {travel_purpose}, Supervisor Remarks: {supervisor_note}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee.employee_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return travel_title
  except Exception as e:
        print(f"Error sending OTP email: {e}")

def send_travel_expenses_mail(supervisor_email, travel_title, employee, travel_applied_on, travel_expenses_amount, expenses_description):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="TRAVEL EXPENSES",
            body=f"Travel Expenses of: {travel_title}  from {employee.employee_first_name} {employee.employee_second_name} applied on {travel_applied_on} incurred the "
                 f"following expenses : {travel_expenses_amount} "
                 f"Description: {expenses_description}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[supervisor_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return travel_title
  except Exception as e:
        print(f"Error sending OTP email: {e}")

def send_approve_expenses_mail(travel_title, employee, travel_applied_on, travel_purpose):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="TRAVEL EXPENSES APPROVAL",
            body=f"Your travel request: {travel_title}  from {employee.employee_first_name} {employee.employee_second_name} applied on {travel_applied_on}  "
                 f"has been APPROVED!"
                 f"Travel details: {travel_purpose}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee.employee_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return travel_title
  except Exception as e:
        print(f"Error sending OTP email: {e}")

def send_decline_expenses_mail(travel_title, employee, travel_applied_on, travel_purpose):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="TRAVEL EXPENSES DECLINE",
            body=f"Your travel request: {travel_title}  from {employee.employee_first_name} {employee.employee_second_name} applied on {travel_applied_on}  "
                 f"has been APPROVED!"
                 f"Travel details: {travel_purpose}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee.employee_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return travel_title
  except Exception as e:
        print(f"Error sending OTP email: {e}")
