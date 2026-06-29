from django.db import models
from students.models import Student, Class
from attendance.models import Subject
from accounts.models import User

class Exam(models.Model):
    EXAM_TYPE = [
        ('internal', 'Internal Exam'),
        ('external', 'External / University Exam'),
        ('practical', 'Practical Exam'),
        ('oral', 'Oral Exam'),
        ('term', 'Term Exam'),
        ('unit', 'Unit Test'),
    ]
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    academic_year = models.CharField(max_length=10)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.class_group}"

class SubjectMarks(models.Model):
    GRADE_CHOICES = [
        ('O', 'O - Outstanding (≥80)'),
        ('A+', 'A+ - Excellent (75-79)'),
        ('A', 'A - Very Good (70-74)'),
        ('B+', 'B+ - Good (65-69)'),
        ('B', 'B - Above Average (60-64)'),
        ('C', 'C - Average (55-59)'),
        ('D', 'D - Pass (50-54)'),
        ('F', 'F - Fail (<50)'),
        ('AB', 'AB - Absent'),
    ]

    # Passing marks per exam type:
    # internal  → max 25, pass = 15
    # prelim / external (presem) → max 75, pass = 30
    # practical → max 30, pass = 30 (handled in PracticalMarks)
    PASSING_MARKS_MAP = {
        'internal': (25, 15),   # (max_marks, passing_marks)
        'external': (75, 30),   # presem / university
        'term':     (75, 30),
        'unit':     (25, 15),
        'oral':     (25, 15),
        'practical':(30, 30),
    }

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_marks = models.DecimalField(max_digits=6, decimal_places=2, default=25)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, default=15)
    is_absent = models.BooleanField(default=False)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    entered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['exam', 'student', 'subject']

    def get_default_marks_for_exam(self):
        """Return (max_marks, passing_marks) based on linked exam type."""
        exam_type = self.exam.exam_type if self.exam_id else 'internal'
        return self.PASSING_MARKS_MAP.get(exam_type, (25, 15))

    @property
    def is_pass(self):
        """True if student passed this subject."""
        if self.is_absent or self.marks_obtained is None:
            return False
        return float(self.marks_obtained) >= float(self.passing_marks)

    def save(self, *args, **kwargs):
        # Auto-set max_marks & passing_marks from exam type if not explicitly overridden
        if self.exam_id:
            exam_type = self.exam.exam_type
            default_max, default_pass = self.PASSING_MARKS_MAP.get(exam_type, (25, 15))
            # Only override if still at old generic default (35) or unset
            if float(self.passing_marks) == 35 or float(self.passing_marks) == 15:
                self.passing_marks = default_pass
            if float(self.max_marks) == 100 or float(self.max_marks) == 25:
                self.max_marks = default_max

        if self.marks_obtained is not None and not self.is_absent:
            obtained = float(self.marks_obtained)
            max_m = float(self.max_marks)
            passing = float(self.passing_marks)

            if obtained < passing:
                # Failed — assign F regardless of percentage
                self.grade = 'F'
            else:
                # Passed — calculate grade from percentage of max_marks
                pct = obtained / max_m * 100
                if pct >= 80:   self.grade = 'O'
                elif pct >= 75: self.grade = 'A+'
                elif pct >= 70: self.grade = 'A'
                elif pct >= 65: self.grade = 'B+'
                elif pct >= 60: self.grade = 'B'
                elif pct >= 55: self.grade = 'C'
                else:           self.grade = 'D'
        elif self.is_absent:
            self.grade = 'AB'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}/{self.max_marks}"

class PracticalMarks(models.Model):
    # Practical: max 30, pass = 30 (full marks required to pass)
    PRACTICAL_PASS = 30

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='practical_marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='practical_marks')
    academic_year = models.CharField(max_length=10)
    journal_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    viva_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    experiment_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    passing_marks = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['student', 'subject', 'academic_year']

    @property
    def total_marks(self):
        return self.journal_marks + self.viva_marks + self.experiment_marks

    @property
    def is_pass(self):
        """Pass only if total_marks >= passing_marks (30)."""
        return float(self.total_marks) >= float(self.passing_marks)

    def __str__(self):
        return f"{self.student} - {self.subject} Practical"
