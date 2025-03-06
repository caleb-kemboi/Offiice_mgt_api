from employee_travels.models import Travels, Employee
from services.serviceBase import ServiceBase
from utils.models import User, Roles, Session, ForgotPassword
from deliveries.models import Deliveries
from visitors.models import Visits


class UserService(ServiceBase):
    manager = User.objects

class SessionService(ServiceBase):
    manager = Session.objects

class DeliveryService(ServiceBase):
    manager = Deliveries.objects

class EmployeeTravelService(ServiceBase):
    manager = Travels.objects

class EmployeeService(ServiceBase):
       manager = Employee.objects

class VisitsService(ServiceBase):
      manager = Visits.objects
