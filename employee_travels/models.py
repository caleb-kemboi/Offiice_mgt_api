from django.db import models
from django.conf import settings
from django.utils import timezone
User = settings.AUTH_USER_MODEL
from utils.models import BaseModel, Status


#sort supervisor

class Employee(models.Model):
    employee_first_name = models.CharField(max_length=200)
    employee_second_name = models.CharField(max_length=200)
    employee_email = models.CharField(max_length=200, unique=True)
    employee_phone = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="subordinates",
        null=True,
        blank=True
    )
    is_supervisor = models.BooleanField(default=False)  # Marks if the employee is a supervisor

    def __str__(self):
        return f"{self.employee_first_name} {self.employee_second_name} ({self.employee_email})"



class Travels(BaseModel):
    travel_title = models.CharField(max_length=200)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    travel_applied_on = models.DateTimeField(auto_now_add=True)
    travel_purpose = models.CharField(max_length=200)
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    travel_destination = models.CharField(max_length=50)
    mode_of_transport = models.CharField(max_length=100)
    travel_budget = models.CharField(max_length=100)
    travel_approval_status = models.CharField(max_length=20)
    supervisor_note = models.CharField(max_length=400, blank=True, null=True)

    date_expenses_submitted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    travel_expenses_amount = models.CharField(max_length=20, blank=True, null=True)
    expenses_description = models.TextField(blank=True, null=True)
    expenses_date_submitted = models.DateField(blank=True, null=True)
    expenses_approval_Status = models.CharField(max_length=50)


    def __str__(self):
        return self.travel_title



