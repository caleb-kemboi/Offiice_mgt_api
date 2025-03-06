from django.db import models
from django.db.models import CASCADE
from utils.models import BaseModel
from employee_travels.models import Employee


class Deliveries(BaseModel):
    status = models.CharField(max_length=50)
    item_name = models.CharField(max_length = 200)
    sender_name = models.CharField(max_length=200)
    delivery_description = models.CharField(max_length=200)
    employee = models.ForeignKey(Employee, on_delete=CASCADE)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    pickup_date = models.DateTimeField(blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender_name} - {self.delivery_description}"


