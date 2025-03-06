from django.core.mail import EmailMultiAlternatives
from office_mgt import settings


def send_delivery_mail(item_name, sender_name,employee_email,
                     delivery_description, delivery_date):
  try:

    #html_content = render_to_string('', {'otp': otp})
    email = EmailMultiAlternatives(
            subject="Your Have Received a Package Delivery",
            body=f"Your have {item_name} delivery from {sender_name} on {delivery_date} "
                 f"Delivery details: {delivery_description}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee_email],
        )
    #mail.attach_alternative(html_content, "text/html")
    email.send()
    return item_name
  except Exception as e:
        print(f"Error sending OTP email: {e}")

