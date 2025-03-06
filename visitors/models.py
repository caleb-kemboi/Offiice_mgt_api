from django.utils import timezone

from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


from employee_travels.models import Employee

from utils.models import  BaseModel



#Visits model
class Visits(BaseModel):
  visit_purpose = models.CharField(max_length=200)
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
  visit_date = models.DateTimeField()
  visitor_checked_out = models.BooleanField(default=False, null=True)
  visitor_first_name = models.CharField(max_length=200)
  visitor_last_name = models.CharField(max_length=200)
  visitor_phone = models.CharField(max_length=15)
  visitor_email = models.CharField(max_length=15)
  visit_time = models.TimeField()
  checkout_time = models.TimeField(null=True, blank=True)

  def __str__(self):
   return f"{self.visitor_first_name} - {self.visitor_last_name} - {self.visit_date}"



