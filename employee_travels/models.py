from django.db import models
from utils.models import BaseModel, User


class Travels(BaseModel):
    travel_title = models.CharField(max_length=200)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
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



