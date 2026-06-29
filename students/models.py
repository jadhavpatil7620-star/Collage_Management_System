from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    head = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g., FY, SY, TY
    division = models.CharField(max_length=5)  # A, B, C
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')
    academic_year = models.CharField(max_length=10)  # e.g., 2024-25
    class_teacher = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ['name', 'division', 'department', 'academic_year']
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.name} - {self.division} ({self.department.code}) {self.academic_year}"

class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('passed', 'Passed Out'), ('dropped', 'Dropped')]

    prn = models.CharField(max_length=20, unique=True, verbose_name='PRN')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    aadhar_no = models.CharField(max_length=12, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=20, blank=True)  # OBC, SC, ST, Open
    blood_group = models.CharField(max_length=5, blank=True)

    # Academic
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    admission_date = models.DateField()
    admission_no = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Parent/Guardian
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=15, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_relation = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.prn})"

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(p for p in parts if p)
