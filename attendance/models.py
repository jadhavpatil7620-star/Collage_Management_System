from django.db import models
from students.models import Student, Class
from accounts.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    is_practical = models.BooleanField(default=False)
    max_lectures = models.IntegerField(default=60)

    def __str__(self):
        return f"{self.name} ({self.code})"

class AttendanceSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    lecture_no = models.IntegerField(default=1)
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sessions_taken')
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['subject', 'date', 'lecture_no']
        ordering = ['-date']

    def __str__(self):
        return f"{self.subject} - {self.date}"

class Attendance(models.Model):
    STATUS_CHOICES = [('P', 'Present'), ('A', 'Absent'), ('L', 'Leave')]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student} - {self.session.date} - {self.status}"
