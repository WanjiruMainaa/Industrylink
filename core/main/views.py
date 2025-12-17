from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import RegisterForm, ProjectForm, ProfileEditForm
from .models import StudentProfile, Project, Mentor, Freelancer, Organization
from django.contrib.auth.models import User
from .models import UserProfile
from django_daraja.mpesa.core import MpesaClient


def home(request):
    return render(request, 'main/home.html')

def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        user_type = request.POST.get('user_type', 'student')
        
        if form.is_valid():
            try:
                # 1. Creates the User (Username, Email, Password)
                user = form.save(commit=False)
                user.save()
                
                # 2. Creates the UserProfile (Role + Phone)
                phone = form.cleaned_data.get('phone', '')
                UserProfile.objects.create(
                    user=user,
                    role=user_type,
                    phone=phone
                )
                
                email = form.cleaned_data['email']
                
                # 3. Creates the Specific Profile based on Role
                if user_type == 'student':
                    StudentProfile.objects.create(
                        user=user,
                        institution=form.cleaned_data.get('institution', ''),
                        course=form.cleaned_data.get('course', ''),
                        year_of_study=form.cleaned_data.get('year_of_study', 1),
                        email=email,
                        bio='',
                        skills=''
                    )
                
                elif user_type == 'mentor':
                    Mentor.objects.create(
                        user=user,
                        full_name=f"{user.first_name} {user.last_name}",
                        job_title=form.cleaned_data.get('job_title', ''),
                        company=form.cleaned_data.get('company', ''),
                        linkedin=form.cleaned_data.get('linkedin', ''),
                        expertise_area=form.cleaned_data.get('expertise_area', 'technology'),
                        years_of_experience=form.cleaned_data.get('years_of_experience', 0),
                        availability='Available',
                        bio='Mentor profile',
                        email=email
                    )
                
                elif user_type == 'freelancer':
                    Freelancer.objects.create(
                        user=user,
                        full_name=f"{user.first_name} {user.last_name}",
                        profession=form.cleaned_data.get('profession', ''),
                        specialization=form.cleaned_data.get('specialization', ''),
                        years_of_experience=form.cleaned_data.get('years_of_experience', 0),
                        email=email,
                        bio='Freelancer profile'
                    )
                
                elif user_type == 'organization':
                    Organization.objects.create(
                        user=user,
                        organization_name=form.cleaned_data.get('organization_name'),
                        organization_type=form.cleaned_data.get('organization_type', ''),
                        industry=form.cleaned_data.get('industry', ''),
                        website=form.cleaned_data.get('website', ''),
                        email=email,
                        bio='Organization profile'
                    )
                
                # 4. Logs them in and redirects
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome {user.first_name}! Account created.')
                return redirect('main:dashboard')
                
            except Exception as e:
                user.delete()
                print(f"Error: {e}")
                messages.error(request, f"Registration failed: {str(e)}")
                return render(request, 'main/register.html', {'form': form})
        
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'main/register.html', {'form': form})
    
    else:
        form = RegisterForm()
    
    return render(request, 'main/register.html', {'form': form})


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            check_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
            return render(request, 'main/login.html')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('main:dashboard')
        else:
            messages.error(request, "Incorrect username or password")
    
    return render(request, 'main/login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('main:home')

@login_required(login_url='main:login')
def dashboard(request):
    # --- CHECKS IF USER IS ADMIN ---
    if request.user.is_staff or request.user.is_superuser:
        # 1. Gathers Counts
        context = {
            'total_users': User.objects.count(),
            'total_students': StudentProfile.objects.count(),
            'total_mentors': Mentor.objects.count(),
            'total_freelancers': Freelancer.objects.count(),
            'total_organizations': Organization.objects.count(),
            'total_projects': Project.objects.count(),
            
            # 2. Recent Activity - Who logged in recently?
            # Filter for users who have a last_login date set
            'recent_logins': User.objects.filter(last_login__isnull=False).order_by('-last_login')[:5],
            
            # 3. Recent Activity - Who added a project?
            'recent_projects': Project.objects.select_related('student__user').order_by('-created_at')[:5],
        }
        # RenderS the dedicated Admin Dashboard template
        return render(request, 'main/admin_dashboard.html', context)

    # --- LOGIC FOR NORMAL USERS (Students, Mentors, freelancers.) ---
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_role = user_profile.role
    except UserProfile.DoesNotExist:
        user_role = 'student'
    
    context = {'user_role': user_role}

    if user_role == 'student':
        try:
            student = StudentProfile.objects.get(user=request.user)
            projects = student.projects.all()
            skills_list = [s.strip() for s in student.skills.split(',') if s.strip()]
            context.update({
                'student': student,
                'projects': projects,
                'skills': skills_list,
                'project_count': projects.count(),
                'completed_projects': projects.filter(status='completed').count(),
            })
        except StudentProfile.DoesNotExist:
            pass
            
    elif user_role == 'mentor':
        try:
            mentor = Mentor.objects.get(user=request.user)
            context.update({
                'mentor': mentor,
                'total_students': StudentProfile.objects.count(),
                'total_projects': Project.objects.count(),
            })
        except Mentor.DoesNotExist:
            pass

    elif user_role in ['freelancer', 'organization']:
        try:
            profile = StudentProfile.objects.get(user=request.user) 
            context.update({
                'available_projects': Project.objects.all()[:10],
                'total_students': StudentProfile.objects.count(),
            })
        except StudentProfile.DoesNotExist:
            pass

    return render(request, 'main/dashboard.html', context)


@login_required
def add_project(request):
    user = request.user
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            
            # ATTACHES TO CORRECT PROFILE
            try:
                if hasattr(user, 'student_profile'):
                    project.student = user.student_profile
                elif hasattr(user, 'freelancer_profile'):
                    project.freelancer = user.freelancer_profile
                elif hasattr(user, 'organization_profile'):
                    project.organization = user.organization_profile
                elif user.is_staff:
                    # Admins can also post, but won't be linked to a profile field
                    pass 
                
                project.save()
                messages.success(request, 'Project created successfully!')
                return redirect('main:dashboard')
                
            except Exception as e:
                messages.error(request, f"Error attaching profile: {e}")
    else:
        form = ProjectForm()

    return render(request, 'projects/add_project.html', {'form': form})



@login_required
def view_project(request, project_id):
    """READ operation for single project"""
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/view_project.html', {'project': project})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user owns this project
    if project.student.user != request.user:
        messages.error(request, 'You can only edit your own projects!')
        return redirect('main:dashboard')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Project updated successfully!')
            return redirect('main:dashboard')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Checks if user owns this project
    if project.student.user != request.user:
        messages.error(request, 'You can only delete your own projects!')
        return redirect('main:dashboard')
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'🗑️ Project "{project_title}" deleted successfully!')
        return redirect('main:dashboard')
    
    return render(request, 'projects/delete_project.html', {'project': project})

from .forms import (
    ProfileEditForm, 
    MentorProfileEditForm, 
    FreelancerProfileEditForm, 
    OrganizationProfileEditForm
)

@login_required
def editProfile(request):
    try:
        user_profile = request.user.profile
        role = user_profile.role
    except Exception:
        if request.user.is_staff:
            messages.info(request, "Admin settings are in the Admin Panel.")
        else:
            messages.error(request, "User profile data is missing.")
        return redirect('main:dashboard')

    profile_instance = None
    FormClass = None
    template_name = 'main/editProfile.html'

    if role == 'student':
        profile_instance, created = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'year_of_study': 1,
                'email': request.user.email
            }
        )
        FormClass = ProfileEditForm

    elif role == 'mentor':
        profile_instance, created = Mentor.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': f"{request.user.first_name} {request.user.last_name}",
                'email': request.user.email,
                'expertise_area': 'technology', 
                'years_of_experience': 0,       
                'availability': 'Available'
            }
        )
        FormClass = MentorProfileEditForm

    elif role == 'freelancer':
        profile_instance, created = Freelancer.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': f"{request.user.first_name} {request.user.last_name}",
                'email': request.user.email,
                'years_of_experience': 0
            }
        )
        FormClass = FreelancerProfileEditForm

    elif role == 'organization':
        profile_instance, created = Organization.objects.get_or_create(
            user=request.user,
            defaults={
                'organization_name': request.user.username, 
                'email': request.user.email,
                'organization_type': 'Startup' 
            }
        )
        FormClass = OrganizationProfileEditForm

    # 4. Handles the Form Logic
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('main:dashboard')
        else:
             messages.error(request, 'Please correct the errors below.')
    else:
        form = FormClass(instance=profile_instance)

    return render(request, template_name, {'form': form, 'user_role': role})


def projects(request):
    all_projects = Project.objects.all().order_by('-created_at')
    is_mentor = request.user.is_authenticated and hasattr(request.user, 'mentor')
    
    return render(request, 'main/projects.html', {
        'projects': all_projects,
        'is_mentor': is_mentor
    })


def mentor_list(request):
    all_mentors = Mentor.objects.all()
    return render(request, 'main/mentor.html', {'mentors': all_mentors})


@login_required(login_url='main:login')
def skill_gap_analyser(request):
    results = None
    
    role_skills = {
        'Full Stack Developer': ['Python', 'Django', 'JavaScript', 'React', 'SQL', 'Git', 'HTML/CSS'],
        'Data Analyst': ['Python', 'SQL', 'Excel', 'Data Visualization'],
        'UI/UX Designer': ['Figma', 'Adobe XD', 'User Research', 'HTML/CSS'],
        'Mobile Developer': ['Java', 'Kotlin', 'API Integration'],
        'DevOps Engineer': ['Linux', 'Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Python', 'Git'],
        'Finance' : ['Financial modelling', 'Accounting principles', 'Risk management', 'Proficiency in Tech'],
        'AI/ML Engineer': ['Python', 'Tensorflow', 'PyTorch', 'Math', 'Statistics', 'Data Engineering', 'MLOps', 'Neural Networks'],

    }
    
    if request.method == 'POST':
        target_role = request.POST.get('target_role')
        user_skills_input = request.POST.get('user_skills', '')
        user_skills = [skill.strip() for skill in user_skills_input.split(',') if skill.strip()]
        
        if target_role in role_skills:
            required_skills = role_skills[target_role]
            user_skills_lower = [skill.lower() for skill in user_skills]
            
            matching_skills = [s for s in required_skills if s.lower() in user_skills_lower]
            missing_skills = [s for s in required_skills if s.lower() not in user_skills_lower]
            
            results = {
                'target_role': target_role,
                'matching_skills': matching_skills,
                'missing_skills': missing_skills,
                'progress_percentage': int((len(matching_skills) / len(required_skills)) * 100),
            }
    
    return render(request, 'main/skill.html', {
        'roles': role_skills.keys(),
        'results': results
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        messages.success(request, f'Thanks {name}! Your message has been received.')
        return redirect('main:contact')
    
    return render(request, 'main/contact.html')


def MpesaPayment(request):
    mentors = Mentor.objects.all()
    
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        amount = int(float(request.POST.get('amount')))
        phone_number = request.POST.get('phone_number')
        phone_number = request.POST.get('phone_number')
        if phone_number.startswith('0'):
            phone_number = '+254' + phone_number[1:]
        elif phone_number.startswith('+254'):
            phone_number = phone_number[1:]

        cl = MpesaClient()
        account_reference = 'IndustryLink'
        callback_url = 'https://api.darajambili.com/express-payment'
        
        if payment_type == 'mentor_session':
            mentor_id = request.POST.get('mentor_id')
            try:
                mentor = Mentor.objects.get(id=mentor_id)
                transaction_desc = f'Mentorship with {mentor.full_name}'
                response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
                messages.success(request, f'Payment initiated! Check your phone.')
            except Mentor.DoesNotExist:
                messages.error(request, 'Mentor not found.')
        
        elif payment_type == 'tip_student':
            transaction_desc = 'Student Tip'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            messages.success(request, f'Tip sent!')
        
        elif payment_type == 'donation':
            transaction_desc = 'Donation'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            messages.success(request, 'Thank you for donating!')
        
        return redirect('main:payment')
    
    return render(request, 'main/payment.html', {'mentors': mentors})