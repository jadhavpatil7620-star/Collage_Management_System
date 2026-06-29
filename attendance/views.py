from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Subject, AttendanceSession, Attendance
from students.models import Student, Class
from .forms import AttendanceSessionForm, SubjectForm
import json

@login_required
def attendance_dashboard(request):
    classes = Class.objects.all()
    subjects = Subject.objects.select_related('class_group').all()
    if request.user.role == 'staff':
        subjects = subjects.filter(teacher=request.user)
    return render(request, 'attendance/dashboard.html', {'classes': classes, 'subjects': subjects})

@login_required
def take_attendance(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    students = Student.objects.filter(current_class=subject.class_group, status='active')
    if request.method == 'POST':
        date = request.POST.get('date')
        lecture_no = request.POST.get('lecture_no', 1)
        session, created = AttendanceSession.objects.get_or_create(
            subject=subject, date=date, lecture_no=lecture_no,
            defaults={'taken_by': request.user}
        )
        for student in students:
            status = request.POST.get(f'status_{student.pk}', 'A')
            Attendance.objects.update_or_create(
                session=session, student=student,
                defaults={'status': status}
            )
        messages.success(request, f'Attendance saved for {date}!')
        return redirect('attendance_dashboard')
    return render(request, 'attendance/take_attendance.html', {'subject': subject, 'students': students})

@login_required
def attendance_report(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class')
    selected_subject = request.GET.get('subject')
    report_data = []
    subjects = []
    if selected_class:
        subjects = Subject.objects.filter(class_group_id=selected_class)
    if selected_class and selected_subject:
        students = Student.objects.filter(current_class_id=selected_class, status='active')
        subject = get_object_or_404(Subject, pk=selected_subject)
        total_sessions = AttendanceSession.objects.filter(subject=subject).count()
        for student in students:
            present = Attendance.objects.filter(
                session__subject=subject, student=student, status='P'
            ).count()
            percentage = round((present / total_sessions * 100), 2) if total_sessions > 0 else 0
            report_data.append({
                'student': student,
                'present': present,
                'absent': total_sessions - present,
                'total': total_sessions,
                'percentage': percentage,
                'low': percentage < 75
            })
    return render(request, 'attendance/report.html', {
        'classes': classes, 'subjects': subjects,
        'report_data': report_data,
        'selected_class': selected_class,
        'selected_subject': selected_subject
    })

@login_required
def subject_list(request):
    subjects = Subject.objects.select_related('class_group__department', 'teacher').all()
    return render(request, 'attendance/subject_list.html', {'subjects': subjects})

@login_required
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'attendance/subject_form.html', {'form': form})
