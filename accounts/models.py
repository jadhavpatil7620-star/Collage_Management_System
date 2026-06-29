from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('principal', 'Principal'),
        ('staff', 'Staff / Teacher'),
        ('clerk', 'Clerk'),
        ('accountant', 'Accountant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_principal(self):
        return self.role == 'principal'

    @property
    def is_staff_member(self):
        return self.role == 'staff'

    @property
    def is_clerk(self):
        return self.role == 'clerk'

    @property
    def is_accountant(self):
        return self.role == 'accountant'

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'staff'}
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['teacher', 'subject']

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.subject.name}"