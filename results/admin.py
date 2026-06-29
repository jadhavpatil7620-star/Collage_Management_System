from django.contrib import admin
from .models import Exam, SubjectMarks, PracticalMarks

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'class_group', 'academic_year', 'is_active']
    list_filter = ['exam_type', 'is_active', 'class_group__department']

@admin.register(SubjectMarks)
class SubjectMarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'marks_obtained', 'max_marks', 'grade']
    list_filter = ['exam', 'grade']

@admin.register(PracticalMarks)
class PracticalMarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'academic_year', 'total_marks', 'max_marks']
