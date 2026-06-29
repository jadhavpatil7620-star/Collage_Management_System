from django.contrib import admin
from .models import BonafideCertificate, LeavingCertificate

@admin.register(BonafideCertificate)
class BonafideAdmin(admin.ModelAdmin):
    list_display = ['certificate_no', 'student', 'purpose', 'issued_date', 'issued_by']
    list_filter = ['purpose', 'issued_date']
    search_fields = ['certificate_no', 'student__first_name', 'student__prn']

@admin.register(LeavingCertificate)
class LeavingCertAdmin(admin.ModelAdmin):
    list_display = ['certificate_no', 'student', 'leaving_date', 'conduct', 'issued_date']
    search_fields = ['certificate_no', 'student__first_name', 'student__prn']
