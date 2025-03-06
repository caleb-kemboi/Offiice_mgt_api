import random
import uuid
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


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


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.CharField(max_length=20, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.FileField(upload_to="media/profile/profilePics", max_length=255, null=True, blank=True)
    is_otp_verified = models.BooleanField(default=False)
    is_reset_otp_verified = models.BooleanField(default=False)


    # Required fields for authentication and admin
    is_active = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Enables admin access
    is_superuser = models.BooleanField(default=False)  # Enables all permissions

    def generate_otp(self):
        """Generate a random 6-digit OTP"""
        return str(random.randint(100000, 999999))

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    reset_otp = models.CharField(max_length=6, blank=True, null=True)
    reset_otp_expiry = models.DateTimeField(blank=True, null=True)


    objects = CustomUserManager()  # Attach the custom manager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


def assign_user_role(user):
    if user.is_supervisor:
        group, _ = Group.objects.get_or_create(name="Supervisors")
        user.groups.add(group)
    else:
        group, _ = Group.objects.get_or_create(name="Employees")
        user.groups.add(group)


# OTP & Password Reset Models
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