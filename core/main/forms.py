from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile, Project

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    institution = forms.CharField(
        max_length=200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g Strathmore University'}))
    course = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g Information Technology'})) 
    year_of_study = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g 3', 'min': '1', max:'6'}))
    
    job_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Senior Software Engineer'
        })
    )
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Safaricom PLC'
        })
    )
    years_of_experience = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 5',
            'min': '0'
        }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [ 'institution', 'course', 'year_of_study', 'bio', 'phone',]
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your university or institution'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your course/major'
            }),
            'year_of_study': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '6'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself, your interests, and career goals...'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter skills separated by commas (e.g., Python, Django, React, SQL)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 7XX XXX XXX'
            }),
        }
        labels = {
            'bio': 'About You',
            'skills': 'Your Skills (comma-separated)',
            'phone': 'Phone Number',
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description',  'github_link', 'skills_used',  'status', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., E-commerce Website'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what your project does and what problem it solves...'
            }),
            'skills_used': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Technologies and skills used (e.g., Django, Bootstrap)'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername/project-name'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'github_link': 'GitHub Repository Link',
            'skills_used': 'Technologies & Skills Used',
        }
    
    def clean(self):
       
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError('End date cannot be before start date!')
        
        return cleaned_data

