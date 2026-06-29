from django.db import models
from students.models import Student
from accounts.models import User

class FeeStructure(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=10)
    class_group = models.ForeignKey('students.Class', on_delete=models.CASCADE, related_name='fee_structures', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ₹{self.amount} ({self.academic_year})"

class FeePayment(models.Model):
    PAYMENT_MODE = [
        ('cash', 'Cash'),
        ('online', 'Online Transfer'),
        ('cheque', 'Cheque'),
        ('dd', 'Demand Draft'),
    ]
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('pending', 'Pending'),
        ('waived', 'Waived'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE, default='cash')
    receipt_no = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    transaction_id = models.CharField(max_length=50, blank=True)
    cheque_no = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.receipt_no} - {self.student} - ₹{self.amount_paid}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('salary', 'Staff Salary'),
        ('infrastructure', 'Infrastructure'),
        ('equipment', 'Equipment'),
        ('stationery', 'Stationery'),
        ('maintenance', 'Maintenance'),
        ('utility', 'Utility Bills'),
        ('event', 'Events & Activities'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_expenses')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_expenses')
    receipt_file = models.FileField(upload_to='expense_receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.date})"

class ScholarshipGrant(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scholarships')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=10)
    date_awarded = models.DateField()
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.student} - ₹{self.amount}"
