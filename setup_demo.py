"""
Setup script - Run after makemigrations and migrate.
Creates demo users, departments, classes, students, subjects and fee structures.

Usage:
    python manage.py shell < setup_demo.py
    OR
    python setup_demo.py  (from project root, sets DJANGO_SETTINGS_MODULE)
"""

import os, sys, django
from pathlib import Path

# Ensure Django is set up
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_mgmt.settings')
django.setup()

from django.contrib.auth import get_user_model
from students.models import Department, Class, Student
from attendance.models import Subject
from finance.models import FeeStructure
from datetime import date, timedelta
import random

User = get_user_model()

print("🎓 Setting up College Management System demo data...\n")

# ── Users ──────────────────────────────────────────────────────────────────────
users_data = [
    {'username': 'principal', 'password': 'principal@123', 'role': 'principal',
     'first_name': 'Dr. Rajesh',  'last_name': 'Sharma',   'email': 'principal@college.edu',
     'employee_id': 'EMP001', 'department': 'Administration'},
    {'username': 'staff1',    'password': 'staff@123',    'role': 'staff',
     'first_name': 'Prof. Anjali','last_name': 'Patil',    'email': 'anjali@college.edu',
     'employee_id': 'EMP002', 'department': 'Computer Science'},
    {'username': 'staff2',    'password': 'staff@123',    'role': 'staff',
     'first_name': 'Prof. Suresh', 'last_name': 'Kulkarni','email': 'suresh@college.edu',
     'employee_id': 'EMP003', 'department': 'Mathematics'},
    {'username': 'clerk1',    'password': 'clerk@123',    'role': 'clerk',
     'first_name': 'Priya',   'last_name': 'Desai',       'email': 'clerk@college.edu',
     'employee_id': 'EMP004', 'department': 'Administration'},
    {'username': 'accountant1','password':'accountant@123','role': 'accountant',
     'first_name': 'Ravi',    'last_name': 'Joshi',       'email': 'accounts@college.edu',
     'employee_id': 'EMP005', 'department': 'Accounts'},
]

created_users = {}
for ud in users_data:
    u, created = User.objects.get_or_create(username=ud['username'])
    u.set_password(ud['password'])
    for k, v in ud.items():
        if k not in ('username', 'password'):
            setattr(u, k, v)
    u.save()
    created_users[ud['username']] = u
    print(f"  ✅ User: {ud['username']} / {ud['password']}  [{ud['role']}]")

# Superuser for admin panel
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@college.edu', 'admin123',
                                   first_name='Admin', last_name='User', role='principal')
    print("  ✅ Superuser: admin / admin123")

print()

# ── Departments ────────────────────────────────────────────────────────────────
depts_data = [
    {'name': 'Computer Science', 'code': 'CS',  'head': 'Prof. Anjali Patil'},
    {'name': 'Mathematics',      'code': 'MTH', 'head': 'Prof. Suresh Kulkarni'},
    {'name': 'Physics',          'code': 'PHY', 'head': 'Dr. Meena Rao'},
    {'name': 'Commerce',         'code': 'COM', 'head': 'Prof. Vikas Nair'},
]
depts = {}
for dd in depts_data:
    d, _ = Department.objects.get_or_create(code=dd['code'], defaults=dd)
    depts[dd['code']] = d
    print(f"  📚 Department: {d.name}")

print()

# ── Classes ────────────────────────────────────────────────────────────────────
classes_data = [
    ('FY', 'A', 'CS',  '2024-25', 'Prof. Anjali Patil'),
    ('FY', 'B', 'CS',  '2024-25', 'Prof. Suresh Kulkarni'),
    ('SY', 'A', 'CS',  '2024-25', 'Prof. Anjali Patil'),
    ('TY', 'A', 'CS',  '2024-25', 'Prof. Anjali Patil'),
    ('FY', 'A', 'COM', '2024-25', 'Prof. Vikas Nair'),
    ('SY', 'A', 'COM', '2024-25', 'Prof. Vikas Nair'),
]
classes = {}
for name, div, dept_code, yr, teacher in classes_data:
    cls, _ = Class.objects.get_or_create(
        name=name, division=div, department=depts[dept_code], academic_year=yr,
        defaults={'class_teacher': teacher}
    )
    classes[f"{name}{div}{dept_code}"] = cls
    print(f"  🏫 Class: {cls}")

print()

# ── Students ───────────────────────────────────────────────────────────────────
first_names = ['Aarav','Aditi','Akash','Anjali','Arjun','Deepika','Gaurav','Kavita',
               'Manish','Neha','Pranav','Priya','Rahul','Riya','Rohit','Sanjana',
               'Siddharth','Sneha','Suresh','Tanvi']
last_names  = ['Patil','Sharma','Kulkarni','Desai','Joshi','Nair','Rao','Mehta',
               'Gupta','Kumar','Singh','Verma','Iyer','Pillai','Ghosh']

genders = ['M','F']
categories = ['OBC','SC','Open','ST']
blood_groups = ['A+','A-','B+','B-','O+','O-','AB+','AB-']

def rand_phone():
    return '9' + ''.join([str(random.randint(0,9)) for _ in range(9)])

def rand_date(start_year=2000, end_year=2005):
    return date(random.randint(start_year, end_year), random.randint(1,12), random.randint(1,28))

all_classes = list(classes.values())
student_count = 0
for i in range(40):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    mn = random.choice(first_names)
    prn = f"PRN2024{str(i+1).zfill(4)}"
    adm = f"ADM{str(i+1).zfill(4)}"
    gender = random.choice(genders)
    cls = random.choice(all_classes)

    if Student.objects.filter(prn=prn).exists():
        continue

    Student.objects.create(
        prn=prn, first_name=fn, middle_name=mn, last_name=ln,
        gender=gender, date_of_birth=rand_date(),
        address=f"{random.randint(1,999)}, Some Street, Nanded, Maharashtra",
        phone=rand_phone(), email=f"{fn.lower()}.{ln.lower()}@email.com",
        aadhar_no=str(random.randint(100000000000, 999999999999)),
        caste='Hindu', category=random.choice(categories),
        blood_group=random.choice(blood_groups),
        current_class=cls, admission_date=date(2024, 6, random.randint(1,30)),
        admission_no=adm, status='active',
        father_name=f"{random.choice(first_names)} {ln}",
        father_phone=rand_phone(), father_occupation=random.choice(['Farmer','Business','Service','Labour']),
        mother_name=f"{random.choice(first_names)} {ln}",
        mother_phone=rand_phone(),
    )
    student_count += 1

print(f"  👨‍🎓 Created {student_count} students")

# ── Subjects ───────────────────────────────────────────────────────────────────
subjects_data = [
    ('Data Structures',      'CS101', 'FYACS',  False, 60),
    ('Programming in C',     'CS102', 'FYACS',  False, 60),
    ('Mathematics-I',        'MTH101','FYACS',  False, 48),
    ('Physics Lab',          'PHY101','FYACS',  True,  30),
    ('Computer Networks',    'CS201', 'SYACS',  False, 60),
    ('Database Management',  'CS202', 'SYACS',  False, 60),
    ('DBMS Lab',             'CS203', 'SYACS',  True,  30),
    ('Software Engineering', 'CS301', 'TYACS',  False, 60),
    ('Project',              'CS302', 'TYACS',  True,  0),
    ('Accountancy-I',        'COM101','FYACOM', False, 60),
    ('Economics',            'COM102','FYACOM', False, 60),
]
staff1 = created_users['staff1']
staff2 = created_users['staff2']
for sname, scode, cls_key, is_prac, max_lec in subjects_data:
    if cls_key in classes:
        Subject.objects.get_or_create(
            code=scode,
            defaults={
                'name': sname, 'class_group': classes[cls_key],
                'teacher': staff1 if 'CS' in scode else staff2,
                'is_practical': is_prac, 'max_lectures': max_lec,
            }
        )
print(f"  📖 Subjects created")

# ── Fee Structures ─────────────────────────────────────────────────────────────
fee_structs = [
    ('Tuition Fee - CS FY', '2024-25', 25000),
    ('Tuition Fee - CS SY', '2024-25', 28000),
    ('Tuition Fee - CS TY', '2024-25', 30000),
    ('Tuition Fee - COM FY','2024-25', 18000),
    ('Exam Fee',            '2024-25',  2500),
    ('Library Fee',         '2024-25',   500),
    ('Lab Fee',             '2024-25',  3000),
    ('Sports Fee',          '2024-25',   300),
]
for fname, yr, amt in fee_structs:
    FeeStructure.objects.get_or_create(
        name=fname, academic_year=yr,
        defaults={'amount': amt, 'is_active': True}
    )
print(f"  💰 Fee structures created")

print("\n" + "="*60)
print("✅  SETUP COMPLETE!")
print("="*60)
print("\nLogin Credentials:")
print("─" * 40)
print("  Admin Panel:  admin        / admin123")
print("  Principal:    principal    / principal@123")
print("  Staff:        staff1       / staff@123")
print("  Clerk:        clerk1       / clerk@123")
print("  Accountant:   accountant1  / accountant@123")
print("─" * 40)
print("\nRun: python manage.py runserver")
print("Open: http://127.0.0.1:8000/\n")
