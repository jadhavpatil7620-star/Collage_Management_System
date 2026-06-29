from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'role', 'email', 'phone', 'department', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    fieldsets = UserAdmin.fieldsets + (
        ('College Info', {'fields': ('role', 'phone', 'address', 'department', 'employee_id', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('College Info', {'fields': ('role', 'first_name', 'last_name', 'email', 'phone', 'department', 'employee_id')}),
    )
