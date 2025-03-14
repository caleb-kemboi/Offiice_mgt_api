from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import random
import uuid
from django.utils import timezone

class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        abstract = True

class Roles(BaseModel):
    def __str__(self):
        return self.name

class Permissions(BaseModel):
    def __str__(self):
        return self.name

class Status(BaseModel):
    def __str__(self):
        return self.name

class RolePermissions(BaseModel):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    permissions = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password, role='employee', supervisor=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        if role == 'employee' and supervisor is None:
            raise ValueError("Employees must have a supervisor.")

        user = self.model(email=email, role=role, supervisor=supervisor, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Remove the username field
    username = None

    # Email becomes the unique identifier
    email = models.EmailField(max_length=100, unique=True)

    # Define the authentication field and required fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('receptionist', 'Receptionist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    supervisor = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='supervised_employees'
    )

    # Additional fields
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.CharField(max_length=20, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.FileField(upload_to="media/profile/profilePics", max_length=255, null=True, blank=True)
    is_otp_verified = models.BooleanField(default=False)
    is_reset_otp_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    reset_otp = models.CharField(max_length=6, blank=True, null=True)
    reset_otp_expiry = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    def is_admin(self):
        return self.role == 'admin'

    def is_employee(self):
        return self.role == 'employee'

    def is_receptionist(self):
        return self.role == 'receptionist'

    def is_supervisor(self):
        """A user is a supervisor if they have employees assigned to them"""
        return self.is_employee() and self.supervised_employees.exists()

    def generate_otp(self):
        """Generate a random 6-digit OTP"""
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.email} ({self.role})"

# Utility for assigning user roles to groups
def assign_user_role(user):
    if user.is_supervisor():
        group, _ = Group.objects.get_or_create(name="Supervisors")
        user.groups.add(group)
    else:
        group, _ = Group.objects.get_or_create(name="Employees")
        user.groups.add(group)

# OTP & Password Reset Models (omitted for brevity)
class Session(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def expire_otp(self):
        self.is_valid = False
        self.save()

    def is_otp_expired(self):
        return timezone.now() - self.otp_created_at > timezone.timedelta(minutes=15)

class ForgotPassword(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def expire_otp(self):
        self.is_valid = False
        self.save()

    def is_otp_expired(self):
        return timezone.now() - self.otp_created_at > timezone.timedelta(minutes=5)
