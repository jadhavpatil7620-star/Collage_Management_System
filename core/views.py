from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone

@login_required
def dashboard(request):
    from students.models import Student, Class, Department
    from attendance.models import AttendanceSession
    from results.models import Exam
    from finance.models import FeePayment, Expense
    from bonafide.models import BonafideCertificate

    today = timezone.now().date()
    this_month = today.replace(day=1)
    user = request.user

    hour = timezone.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    ctx = {
        'user': user,
        'today': today,
        'greeting': greeting,
        'total_students': Student.objects.filter(status='active').count(),
        'total_classes': Class.objects.count(),
        'total_departments': Department.objects.count(),
        'total_exams': Exam.objects.filter(is_active=True).count(),
        'recent_payments': [],
        'recent_students': [],
        'my_subjects': [],
    }

    if user.role in ['principal', 'clerk']:
        ctx['recent_students'] = Student.objects.filter(status='active').order_by('-created_at')[:5]
        ctx['bonafide_count'] = BonafideCertificate.objects.filter(issued_date__gte=this_month).count()

    if user.role in ['accountant', 'principal']:
        ctx['month_fees'] = FeePayment.objects.filter(payment_date__gte=this_month, status='paid').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        ctx['month_expenses'] = Expense.objects.filter(date__gte=this_month).aggregate(Sum('amount'))['amount__sum'] or 0
        ctx['total_fees'] = FeePayment.objects.filter(status='paid').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        ctx['recent_payments'] = FeePayment.objects.select_related('student').order_by('-created_at')[:8]

    if user.role == 'staff':
        from attendance.models import Subject
        ctx['my_subjects'] = Subject.objects.filter(teacher=user).select_related('class_group')
        ctx['today_sessions'] = AttendanceSession.objects.filter(taken_by=user, date=today).count()

    if user.role == 'principal':
        ctx['bonafide_count'] = BonafideCertificate.objects.filter(issued_date__gte=this_month).count()
        ctx['recent_students'] = Student.objects.filter(status='active').order_by('-created_at')[:5]
        ctx['recent_payments'] = FeePayment.objects.select_related('student').order_by('-created_at')[:8]

    classes_data = Class.objects.annotate(
        student_count=Count('students', filter=Q(students__status='active'))
    ).order_by('name')
    ctx['classes_chart'] = [{'name': f"{c.name}-{c.division}", 'count': c.student_count} for c in classes_data]

    return render(request, 'core/dashboard.html', ctx)

@login_required
def notices(request):
    return render(request, 'core/notices.html')
