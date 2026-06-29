from django.contrib import admin
from .models import Student, Class, Department

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['prn', 'full_name', 'current_class', 'phone', 'status', 'admission_date']
    list_filter = ['status', 'gender', 'current_class__department']
    search_fields = ['prn', 'first_name', 'last_name', 'admission_no', 'father_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'division', 'department', 'academic_year', 'class_teacher']
    list_filter = ['department', 'academic_year']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'head']
