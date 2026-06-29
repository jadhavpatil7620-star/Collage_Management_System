from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import FeeStructure, FeePayment, Expense, ScholarshipGrant
from students.models import Student, Class
from .forms import FeePaymentForm, FeeStructureForm, ExpenseForm
import datetime, uuid

def accountant_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role not in ['accountant', 'principal']:
            messages.error(request, 'Access denied. Accountant role required.')
            return redirect('dashboard')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@login_required
@accountant_required
def finance_dashboard(request):
    today = timezone.now().date()
    this_month = today.replace(day=1)
    total_collected = FeePayment.objects.filter(status='paid').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    month_collected = FeePayment.objects.filter(status='paid', payment_date__gte=this_month).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    month_expenses = Expense.objects.filter(date__gte=this_month).aggregate(Sum('amount'))['amount__sum'] or 0
    recent_payments = FeePayment.objects.select_related('student').order_by('-created_at')[:10]
    pending_students = Student.objects.filter(status='active').exclude(fee_payments__status='paid')[:10]
    return render(request, 'finance/dashboard.html', {
        'total_collected': total_collected,
        'month_collected': month_collected,
        'total_expenses': total_expenses,
        'month_expenses': month_expenses,
        'balance': float(total_collected) - float(total_expenses),
        'recent_payments': recent_payments,
        'pending_students': pending_students,
    })

@login_required
@accountant_required
def collect_fee(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.collected_by = request.user
            if not payment.receipt_no:
                payment.receipt_no = f"RCP{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
            payment.save()
            messages.success(request, f'Fee collected! Receipt #{payment.receipt_no}')
            return redirect('view_receipt', pk=payment.pk)
    else:
        student_id = request.GET.get('student')
        initial = {'payment_date': timezone.now().date()}
        if student_id:
            initial['student'] = student_id
        form = FeePaymentForm(initial=initial)
    students = Student.objects.filter(status='active').order_by('first_name')
    return render(request, 'finance/collect_fee.html', {'form': form, 'students': students})

@login_required
@accountant_required
def view_receipt(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    return render(request, 'finance/receipt.html', {'payment': payment})

@login_required
@accountant_required
def fee_report(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    payments = FeePayment.objects.select_related('student', 'fee_structure').order_by('-payment_date')
    if selected_class:
        payments = payments.filter(student__current_class_id=selected_class)
    if date_from:
        payments = payments.filter(payment_date__gte=date_from)
    if date_to:
        payments = payments.filter(payment_date__lte=date_to)
    total = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    return render(request, 'finance/fee_report.html', {
        'payments': payments, 'classes': classes, 'total': total,
        'selected_class': selected_class, 'date_from': date_from, 'date_to': date_to
    })

@login_required
@accountant_required
def expense_list(request):
    expenses = Expense.objects.select_related('added_by').order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'finance/expense_list.html', {'expenses': expenses, 'total': total})

@login_required
@accountant_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.added_by = request.user
            exp.save()
            messages.success(request, 'Expense recorded!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finance/expense_form.html', {'form': form})

@login_required
def fee_structure_list(request):
    structures = FeeStructure.objects.all()
    return render(request, 'finance/fee_structure_list.html', {'structures': structures})

@login_required
@accountant_required
def fee_structure_add(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure added!')
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm()
    return render(request, 'finance/fee_structure_form.html', {'form': form})

@login_required
@accountant_required
def scholarship_list(request):
    scholarships = ScholarshipGrant.objects.select_related('student').order_by('-date_awarded')
    return render(request, 'finance/scholarship_list.html', {'scholarships': scholarships})
