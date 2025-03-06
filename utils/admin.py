from django.contrib import admin

from utils.models import User, Status, Roles, RolePermissions, Permissions

admin.site.register([User, Status, Roles, RolePermissions, Permissions])