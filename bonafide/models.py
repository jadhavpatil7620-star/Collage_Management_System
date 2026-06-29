from django.db import models
from students.models import Student
from accounts.models import User

class BonafideCertificate(models.Model):
    PURPOSE_CHOICES = [
        ('bank_loan', 'Bank Loan'),
        ('scholarship', 'Scholarship'),
        ('passport', 'Passport'),
        ('visa', 'Visa'),
        ('employment', 'Employment'),
        ('higher_study', 'Higher Study Admission'),
        ('railway_concession', 'Railway Concession'),
        ('general', 'General Purpose'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bonafides')
    certificate_no = models.CharField(max_length=30, unique=True)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES, default='general')
    custom_purpose = models.CharField(max_length=200, blank=True)
    issued_date = models.DateField(auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_bonafides')
    additional_text = models.TextField(blank=True, help_text='Any additional information to include in the certificate')
    is_valid = models.BooleanField(default=True)
    downloaded_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Bonafide #{self.certificate_no} - {self.student}"

class LeavingCertificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leaving_certs')
    certificate_no = models.CharField(max_length=30, unique=True)
    leaving_date = models.DateField()
    reason = models.TextField()
    last_exam = models.CharField(max_length=100, blank=True)
    conduct = models.CharField(max_length=50, default='Good')
    issued_date = models.DateField(auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"LC #{self.certificate_no} - {self.student}"
