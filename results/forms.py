from django import forms
from .models import Exam, SubjectMarks, PracticalMarks

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ['created_by']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

class MarksEntryForm(forms.ModelForm):
    class Meta:
        model = SubjectMarks
        fields = ['marks_obtained', 'max_marks', 'is_absent', 'remarks']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PracticalMarksForm(forms.ModelForm):
    class Meta:
        model = PracticalMarks
        exclude = ['teacher']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
