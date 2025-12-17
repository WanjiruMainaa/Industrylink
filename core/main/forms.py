from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile, Project, Mentor, Organization, Freelancer

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    # Student fields
    institution = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control student-field',
            'placeholder': 'e.g., Strathmore University'
        })
    )

    course = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control student-field',
            'placeholder': 'e.g., Information Technology'
        })
    )
    year_of_study = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control student-field',
            'placeholder': '1-4',
            'min': '1',
            'max': '4'
        })
    )

    # Mentor fields
    job_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mentor-field',
            'placeholder': 'e.g., Senior Software Engineer'
        })
    )
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mentor-field',
            'placeholder': 'e.g., Safaricom PLC'
        })
    )
    years_of_experience = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control mentor-field freelancer-field',
            'placeholder': 'Years of experience',
            'min': '0'
        })
    )
    
    expertise_area = forms.ChoiceField(
        choices=[
            ('', 'Select Expertise'),
            ('technology', 'Technology'),
            ('design', 'Design'),
            ('business', 'Business'),
            ('other', 'Other')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control mentor-field'
        })
    )

    # Freelancer fields
    profession = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control freelancer-field',
            'placeholder': 'e.g., Full Stack Developer'
        })
    )
    specialization = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control freelancer-field',
            'placeholder': 'e.g., Web Development'
        })
    )

    # Organization fields
    organization_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control organization-field',
            'placeholder': 'Organization Name'
        })
    )
    organization_type = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control organization-field',
            'placeholder': 'e.g., NGO, Startup, Corporation'
        })
    )

    industry = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control organization-field',
            'placeholder': 'e.g., Technology, Education'
        })
    )
    
    website = forms.URLField(
    required=False,
    widget=forms.URLInput(attrs={
        'class': 'form-control organization-field',
        'placeholder': 'https://example.org'
    })
    )


    # Common fields
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254 7XX XXX XXX'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
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
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254 7XX XXX XXX'
        })
    )

    class Meta:
        model = StudentProfile
        fields = ['institution', 'course', 'year_of_study', 'skills', 'bio']
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
                'max': '4'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2, ''
                'placeholder': 'Comma separated skills'
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Checks if we are editing an existing profile
        if self.instance and self.instance.pk:
            # Gives access to the related UserProfile to get the saved phone number.
            try:
                self.fields['phone'].initial = self.instance.user.profile.phone
            except AttributeError:
                pass

    # 4. Saves the phone number to the UserProfile table
    def save(self, commit=True):
        # Saves the student data normally
        student = super().save(commit=commit)
        
        # Manually saves the phone number to the sibling UserProfile model
        phone = self.cleaned_data.get('phone')
        if hasattr(student.user, 'profile'):
            student.user.profile.phone = phone
            student.user.profile.save()
            
        return student

class MentorProfileEditForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Mentor
        fields = ['job_title', 'company', 'expertise_area', 'years_of_experience', 'bio', 'linkedin']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise_area': forms.Select(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            try:
                self.fields['phone'].initial = self.instance.user.profile.phone
            except AttributeError:
                pass

    def save(self, commit=True):
        mentor = super().save(commit=commit)
        phone = self.cleaned_data.get('phone')
        if hasattr(mentor.user, 'profile'):
            mentor.user.profile.phone = phone
            mentor.user.profile.save()
        return mentor


class FreelancerProfileEditForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Freelancer
        fields = ['profession', 'specialization', 'years_of_experience', 'bio', 'skills']
        widgets = {
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Comma separated skills'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            try:
                self.fields['phone'].initial = self.instance.user.profile.phone
            except AttributeError:
                pass

    def save(self, commit=True):
        freelancer = super().save(commit=commit)
        phone = self.cleaned_data.get('phone')
        if hasattr(freelancer.user, 'profile'):
            freelancer.user.profile.phone = phone
            freelancer.user.profile.save()
        return freelancer


class OrganizationProfileEditForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Organization
        fields = ['organization_name', 'organization_type', 'industry', 'website', 'bio']
        widgets = {
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_type': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            try:
                self.fields['phone'].initial = self.instance.user.profile.phone
            except AttributeError:
                pass

    def save(self, commit=True):
        org = super().save(commit=commit)
        phone = self.cleaned_data.get('phone')
        if hasattr(org.user, 'profile'):
            org.user.profile.phone = phone
            org.user.profile.save()
        return org


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'skills_used', 'status', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., E-commerce Website'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your project...'
            }),
            'skills_used': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., Django, Bootstrap, PostgreSQL'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/project'
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
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('End date cannot be before start date!')
        
        return cleaned_data