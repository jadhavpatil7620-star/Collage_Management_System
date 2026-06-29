from django import forms
from .models import BonafideCertificate, LeavingCertificate

class BonafideForm(forms.ModelForm):
    class Meta:
        model = BonafideCertificate
        fields = ['student', 'purpose', 'custom_purpose', 'additional_text']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LeavingCertificateForm(forms.ModelForm):
    class Meta:
        model = LeavingCertificate
        exclude = ['certificate_no', 'issued_date', 'issued_by']
        widgets = {
            'leaving_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
