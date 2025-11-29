from django import forms
from models.models import Application , Result , Student , Payment , Admission

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = [
            "amount_paid",
            "payment_method"
        ]
        widgets = {
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "amount_paid": forms.NumberInput(attrs={"class": "form-control"}),
        }