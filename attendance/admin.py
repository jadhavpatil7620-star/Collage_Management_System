from django.contrib import admin
from .models import Subject, AttendanceSession, Attendance

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_group', 'teacher', 'is_practical']
    list_filter = ['is_practical', 'class_group__department']

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'date', 'lecture_no', 'taken_by']
    list_filter = ['date', 'subject__class_group']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status']
    list_filter = ['status']
