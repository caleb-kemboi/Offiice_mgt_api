from django.utils import timezone
from django.db import models
from utils.models import BaseModel, User


#Visits model
class Visits(BaseModel):
  visit_purpose = models.CharField(max_length=200)
  employee = models.ForeignKey(User, on_delete=models.CASCADE)
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



