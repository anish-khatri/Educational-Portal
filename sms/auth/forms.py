from django import forms
from django.contrib.auth.hashers import make_password
from models.models import User
from models.models import Student , School , Subscription

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'phone', 'address', 'dob', 'documents']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'documents': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password'])
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student

class LoginForm(forms.Form):
    email_or_username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none',
            'placeholder': 'Enter Email or Username'
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none',
            'placeholder': 'Enter Password'
        })
    )
    
   
class SchoolRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = School
        fields = ['name', 'address', 'contact', 'image', 'subscription']
        widgets = {
            'subscription': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter School Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter School Address'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter School Contact Number'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}) 
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password']),
            role='school'
        )
        school = super().save(commit=False)
        school.user = user
        if commit:
            school.save()
        return school