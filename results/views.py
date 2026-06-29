from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, SubjectMarks, PracticalMarks
from students.models import Student, Class
from attendance.models import Subject
from .forms import ExamForm, MarksEntryForm, PracticalMarksForm

@login_required
def results_dashboard(request):
    exams = Exam.objects.select_related('class_group').order_by('-start_date')
    classes = Class.objects.all()
    return render(request, 'results/dashboard.html', {'exams': exams, 'classes': classes})

@login_required
def exam_list(request):
    exams = Exam.objects.select_related('class_group__department').all()
    return render(request, 'results/exam_list.html', {'exams': exams})

@login_required
def exam_add(request):
    if request.user.role not in ['principal', 'staff', 'clerk']:
        messages.error(request, 'Access denied.')
        return redirect('results_dashboard')
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            messages.success(request, 'Exam created!')
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'results/exam_form.html', {'form': form, 'title': 'Create Exam'})

@login_required
def enter_marks(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    subjects = Subject.objects.filter(class_group=exam.class_group)
    students = Student.objects.filter(current_class=exam.class_group, status='active')
    selected_subject_id = request.GET.get('subject')
    selected_subject = None
    marks_data = {}
    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, pk=selected_subject_id)
        existing = SubjectMarks.objects.filter(exam=exam, subject=selected_subject)
        marks_data = {m.student_id: m for m in existing}
    if request.method == 'POST':
        selected_subject = get_object_or_404(Subject, pk=request.POST.get('subject_id'))
        # Set max/passing marks based on exam type
        passing_map = {
            'internal': (25, 15),
            'external': (75, 30),
            'term':     (75, 30),
            'unit':     (25, 15),
            'oral':     (25, 15),
            'practical':(30, 30),
        }
        default_max, passing_marks = passing_map.get(exam.exam_type, (25, 15))
        for student in students:
            marks_val = request.POST.get(f'marks_{student.pk}')
            is_absent = request.POST.get(f'absent_{student.pk}') == 'on'
            max_m = request.POST.get(f'max_{student.pk}', default_max)
            SubjectMarks.objects.update_or_create(
                exam=exam, student=student, subject=selected_subject,
                defaults={
                    'marks_obtained': None if is_absent else (marks_val or None),
                    'max_marks': max_m,
                    'passing_marks': passing_marks,
                    'is_absent': is_absent,
                    'entered_by': request.user
                }
            )
        messages.success(request, 'Marks saved successfully!')
        return redirect('enter_marks', exam_id=exam_id)
    return render(request, 'results/enter_marks.html', {
        'exam': exam, 'subjects': subjects, 'students': students,
        'selected_subject': selected_subject, 'marks_data': marks_data
    })

@login_required
def result_report(request):
    classes = Class.objects.all()
    exams = Exam.objects.all()
    selected_exam_id = request.GET.get('exam')
    selected_student_id = request.GET.get('student')
    report = None
    student = None
    if selected_student_id and selected_exam_id:
        student = get_object_or_404(Student, pk=selected_student_id)
        exam = get_object_or_404(Exam, pk=selected_exam_id)
        marks = SubjectMarks.objects.filter(exam=exam, student=student).select_related('subject')

        # Determine passing marks based on exam type
        # internal: max=25, pass=15 | external/presem: max=75, pass=30 | practical: max=30, pass=30
        exam_type = exam.exam_type
        passing_map = {
            'internal': (25, 15),
            'external': (75, 30),
            'term':     (75, 30),
            'unit':     (25, 15),
            'oral':     (25, 15),
            'practical':(30, 30),
        }
        default_max, passing_threshold = passing_map.get(exam_type, (25, 15))

        total_obtained = sum(float(m.marks_obtained or 0) for m in marks if not m.is_absent)
        total_max = sum(float(m.max_marks) for m in marks) or default_max * marks.count()
        percentage = round(total_obtained / total_max * 100, 2) if total_max > 0 else 0

        # PASS only if student scored >= passing_threshold in EVERY subject (not absent)
        all_passed = all(
            float(m.marks_obtained or 0) >= passing_threshold
            for m in marks if not m.is_absent
        )
        # Also fail if any subject is absent
        has_absent = any(m.is_absent for m in marks)

        report = {
            'exam': exam,
            'marks': marks,
            'total_obtained': total_obtained,
            'total_max': total_max,
            'percentage': percentage,
            'passing_threshold': passing_threshold,
            'default_max': default_max,
            'result': 'PASS' if (all_passed and not has_absent) else 'FAIL',
        }
    students = Student.objects.filter(status='active') if selected_exam_id else []
    if selected_exam_id:
        exam_obj = Exam.objects.get(pk=selected_exam_id)
        students = Student.objects.filter(current_class=exam_obj.class_group, status='active')
    return render(request, 'results/report.html', {
        'classes': classes, 'exams': exams, 'report': report,
        'students': students, 'selected_exam': selected_exam_id,
        'selected_student': selected_student_id, 'student': student
    })

@login_required
def practical_marks(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class')
    students = []
    subjects = []
    if selected_class:
        students = Student.objects.filter(current_class_id=selected_class, status='active')
        subjects = Subject.objects.filter(class_group_id=selected_class, is_practical=True)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id')
        academic_year = request.POST.get('academic_year')
        PracticalMarks.objects.update_or_create(
            student_id=student_id, subject_id=subject_id, academic_year=academic_year,
            defaults={
                'journal_marks': request.POST.get('journal_marks', 0),
                'viva_marks': request.POST.get('viva_marks', 0),
                'experiment_marks': request.POST.get('experiment_marks', 0),
                'max_marks': 30,       # Practical max is always 30
                'passing_marks': 30,   # Must score 30/30 to pass
                'teacher': request.user,
                'remarks': request.POST.get('remarks', '')
            }
        )
        messages.success(request, 'Practical marks saved!')
    return render(request, 'results/practical_marks.html', {
        'classes': classes, 'students': students, 'subjects': subjects, 'selected_class': selected_class
    })
