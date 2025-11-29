from django import forms
from models.models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['supporting_documents', 'course']  
        widgets = {
            'supporting_documents': forms.FileInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}), 
        }
