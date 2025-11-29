from django import forms
from models.models import School
from models.models import Subscription

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

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'start_date', 'price', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control' , 'type': 'number','step': '0.01', 'value': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
