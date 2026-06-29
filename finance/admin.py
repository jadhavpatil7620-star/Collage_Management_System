from django.contrib import admin
from .models import FeeStructure, FeePayment, Expense, ScholarshipGrant

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'academic_year', 'class_group', 'is_active']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_no', 'student', 'amount_paid', 'payment_date', 'payment_mode', 'status']
    list_filter = ['status', 'payment_mode', 'payment_date']
    search_fields = ['receipt_no', 'student__first_name', 'student__prn']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'date', 'added_by']
    list_filter = ['category', 'date']

@admin.register(ScholarshipGrant)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'amount', 'academic_year', 'date_awarded']
