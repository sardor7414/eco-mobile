from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'first_name', 'last_name', 'role', 'reset_code', 'is_reset_verified',
                    'is_active', 'is_staff', 'is_active')
