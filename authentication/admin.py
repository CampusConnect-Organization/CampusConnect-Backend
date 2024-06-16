from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "User Type",
            {
                "fields": ("type",),
            },
        ),
    )


admin.site.register(User, UserAdmin)
# admin.site.unregister([Group])
