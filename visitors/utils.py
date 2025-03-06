from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from office_mgt import settings
from services.services import SessionService


def send_host_email(employee_email, visitor_first_name,visitor_last_name,
                     visit_purpose, visit_date):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="Your Have a Visitor Appointment",
            body=f"Your have a meeting for {visit_purpose} with {visitor_first_name} - {visitor_last_name} "
                 f"on {visit_date}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return


  except Exception as e:
        print(f"Error sending OTP email: {e}")

def send_employee_email(visitor_email,
                     visit_purpose, visit_date, employee):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="Your Have a Visitor Appointment",
            body=f"Your have successfully boooked meeting for {visit_purpose} with {employee.employee_first_name} - {employee.employee_first_name} "
                 f"on {visit_date}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[visitor_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return


  except Exception as e:
        print(f"Error sending OTP email: {e}")
