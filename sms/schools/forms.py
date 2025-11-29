from django import forms
from models.models import School, Result, Application , Course

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['user', 'subscription', 'name', 'image', 'address', 'contact', 'status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'subscription': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter School Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter School Address'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter School Contact Number'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
    
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['exam_name', 'total_marks', 'pass_marks', 'obtained_marks', 'status']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Exam Name'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Total Marks'}),
            'pass_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pass Marks'}),
            'obtained_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Obtained Marks'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'duration', 'admission_fees', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Course Description'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Duration (e.g., 2 years)'}),
            'admission_fees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Admission Fee'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }