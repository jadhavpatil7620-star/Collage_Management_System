from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import BonafideCertificate, LeavingCertificate
from students.models import Student
from .forms import BonafideForm, LeavingCertificateForm
import uuid

def principal_or_clerk(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role not in ['principal', 'clerk']:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@login_required
@principal_or_clerk
def bonafide_list(request):
    certificates = BonafideCertificate.objects.select_related('student', 'issued_by').order_by('-issued_date')
    return render(request, 'bonafide/list.html', {'certificates': certificates, 'type': 'bonafide'})

@login_required
@principal_or_clerk
def issue_bonafide(request):
    if request.method == 'POST':
        form = BonafideForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.issued_by = request.user
            cert.certificate_no = f"BNF{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
            cert.save()
            messages.success(request, f'Bonafide Certificate #{cert.certificate_no} issued!')
            return redirect('print_bonafide', pk=cert.pk)
    else:
        student_id = request.GET.get('student')
        form = BonafideForm(initial={'student': student_id} if student_id else {})
    students = Student.objects.filter(status='active').order_by('first_name')
    return render(request, 'bonafide/issue_bonafide.html', {'form': form, 'students': students})

@login_required
@principal_or_clerk
def print_bonafide(request, pk):
    cert = get_object_or_404(BonafideCertificate, pk=pk)
    cert.downloaded_count += 1
    cert.save(update_fields=['downloaded_count'])
    return render(request, 'bonafide/print_bonafide.html', {'cert': cert})

@login_required
@principal_or_clerk
def issue_leaving_cert(request):
    if request.method == 'POST':
        form = LeavingCertificateForm(request.POST)
        if form.is_valid():
            lc = form.save(commit=False)
            lc.issued_by = request.user
            lc.certificate_no = f"LC{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
            lc.save()
            # Update student status
            lc.student.status = 'dropped'
            lc.student.save()
            messages.success(request, f'Leaving Certificate #{lc.certificate_no} issued!')
            return redirect('print_leaving_cert', pk=lc.pk)
    else:
        form = LeavingCertificateForm()
    students = Student.objects.filter(status='active').order_by('first_name')
    return render(request, 'bonafide/issue_leaving_cert.html', {'form': form, 'students': students})

@login_required
@principal_or_clerk
def print_leaving_cert(request, pk):
    cert = get_object_or_404(LeavingCertificate, pk=pk)
    return render(request, 'bonafide/print_leaving_cert.html', {'cert': cert})

@login_required
@principal_or_clerk
def leaving_cert_list(request):
    certs = LeavingCertificate.objects.select_related('student', 'issued_by').order_by('-issued_date')
    return render(request, 'bonafide/list.html', {'certificates': certs, 'type': 'leaving'})
