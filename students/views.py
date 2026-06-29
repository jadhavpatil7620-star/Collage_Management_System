from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Student, Class, Department
from .forms import StudentForm, ClassForm, DepartmentForm

def role_required(*roles):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in roles:
                messages.error(request, 'Access denied.')
                return redirect('dashboard')
            return func(request, *args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@login_required
def student_list(request):
    students = Student.objects.select_related('current_class__department').filter(status='active')
    class_filter = request.GET.get('class')
    search = request.GET.get('q')
    if class_filter:
        students = students.filter(current_class_id=class_filter)
    if search:
        students = students.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) |
            Q(prn__icontains=search) | Q(admission_no__icontains=search)
        )
    classes = Class.objects.all()
    return render(request, 'students/student_list.html', {
        'students': students, 'classes': classes,
        'class_filter': class_filter, 'search': search
    })

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
@role_required('principal', 'clerk')
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

@login_required
@role_required('principal', 'clerk')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})

@login_required
@role_required('principal', 'clerk')
def class_list(request):
    classes = Class.objects.select_related('department').annotate_student_count() if False else Class.objects.select_related('department').all()
    return render(request, 'students/class_list.html', {'classes': classes})

@login_required
@role_required('principal', 'clerk')
def class_add(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class added!')
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'students/class_form.html', {'form': form, 'title': 'Add Class'})

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'students/department_list.html', {'departments': departments})
