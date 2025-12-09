from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProjectForm, ProfileEditForm
from .models import StudentProfile, Project, Mentor
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.
def home(request):
    return render(request, 'main/home.html')


def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        user_type = request.POST.get('user_type', 'student')
        if form.is_valid():
            user = form.save()
            
            # Create StudentProfile based on user type
            if user_type == 'student':
                StudentProfile.objects.create(
                    user=user,
                    institution=form.cleaned_data.get('institution', ''),
                    course=form.cleaned_data.get('course', ''),
                    year_of_study=form.cleaned_data.get('year_of_study', 1),
                    email=form.cleaned_data['email'],
                    bio='Student account',
                )
            elif user_type in ['mentor', 'freelancer']:
                StudentProfile.objects.create(
                    user=user,
                    institution=form.cleaned_data.get('company', ''),
                    course=form.cleaned_data.get('job_title', ''),
                    year_of_study=form.cleaned_data.get('years_of_experience', 0),
                    email=form.cleaned_data['email'],
                    bio=f'{user_type.capitalize()} account',
                )
            elif user_type == 'organization':
                StudentProfile.objects.create(
                    user=user,
                    institution=form.cleaned_data.get('organization_name', ''),
                    course=form.cleaned_data.get('organization_type', ''),
                    year_of_study=0,
                    email=form.cleaned_data['email'],
                    bio='Organization account',
                )
            
            # Login the user
            login(request, user)
            messages.success(request, f'Welcome to IndustryLink, {user.username}!')
            
            # Redirect to dashboard
            return redirect('main:dashboard') 
        else:
            messages.error(request, 'Registration failed. Please check the form.')
            print(form.errors) 
    else:
        form = RegisterForm()
    
    return render(request, 'main/register.html', {'form': form})


@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_mentors = Mentor.objects.count()
    total_students = StudentProfile.objects.filter(year_of_study__gt=0).count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_projects = Project.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_projects': total_projects,
        'total_mentors': total_mentors,
        'total_students': total_students,
        'recent_users': recent_users,
        'recent_projects': recent_projects,
    }
    return render(request, 'main/admin_dashboard.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"""
        New message from IndustryLink Contact Form:
        From: {name}
        Email: {email}
        Subject: {subject}
        Message: 
        {message}
        """

        try:
            send_mail(
                subject=f'IndustryLink Contact: {subject}',
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['mainawanjiru.mymail@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, f'Thanks {name}! Your message has been sent. We will respond as soon as possible!')
        except Exception as e:
            messages.error(request, 'Failed to send message. Please try WhatsApp or call us or visit our offices. We sincerely apologise for any inconvinience caused!')
        return redirect('main:contact')
    
    return render(request, 'main/contact.html')

       

def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('main:dashboard') 
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'main/login.html', {'form': form})


def logoutUser(request):
    context ={}
    logout(request)
    return redirect('main:home')


@login_required(login_url='main:login')
def dashboard(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        projects = student_profile.projects.all()

       
        skills_text = student_profile.skills if student_profile.skills else ''
        skills_list = [skill.strip() for skill in skills_text.split(',') if skill.strip()]

    except StudentProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first')
        return redirect('main/dashboard.html', context)
    context = {
        'student': student_profile,
        'projects': projects,
        'skills': skills_list,
    }
    return render(request, 'main/dashboard.html', context)

def projects_list(request):
    all_projects = Project.objects.all()
    return render(request, 'main/projects.html', {'projects': all_projects})

def projects(request):
    all_projects = Project.objects.all().order_by('-created_at')
    is_mentor = False
    if request.user.is_authenticated:
        is_mentor = hasattr(request.user, 'mentor') or request.user.is_superuser
    
    context = {
        'projects': all_projects,
        'is_mentor': is_mentor
    }
    return render(request, 'main/projects.html', context)
@login_required
def add_project(request):
    # Check if user has a StudentProfile (everyone who registers gets one)
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('main:dashboard')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = student_profile
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('main:dashboard')
    else:
        form = ProjectForm()
    
    return render(request, 'main/projects.html', {'form': form, 'add_mode': True})

@login_required
def mark_project_complete(request, project_id):
    if not (hasattr(request.user, 'mentor') or request.user.is_superuser):
        messages.error(request, 'Only mentors can review projects.')
        return redirect('main:projects')
    
    try:
        project = Project.objects.get(id=project_id)
        project.status = 'completed'
        project.save()
        messages.success(request, f'Project "{project.title}" marked as completed!')
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
    
    return redirect('main:projects')

@login_required
def review_project(request, project_id):
    """View for mentors to review projects"""
    if not (hasattr(request.user, 'mentor') or request.user.is_superuser):
        messages.error(request, 'Only mentors can review projects.')
        return redirect('main:projects')
    
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['ongoing', 'completed', 'paused']:
            project.status = new_status
            project.save()
            messages.success(request, f'Project status updated to {new_status}!')
            return redirect('main:projects')
    
    context = {'project': project}
    return render(request, 'main/review_project.html', context)

@login_required(login_url='main:login')
def editProfile(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please try again later.')
        return redirect('main:home')

    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('main:dashboard')
    else:
        form = ProfileEditForm(instance=student)
    
    return render(request, 'main/editProfile.html', {'form': form})

def mentor_list(request):
    all_mentors = Mentor.objects.all()
    return render(request, 'main/mentor.html', {'mentors': all_mentors})

@login_required(login_url='main:login')
def skill_gap_analyser(request):
    results = None
    
    role_skills = {
        'Full Stack Developer': ['Python', 'Django', 'JavaScript', 'React', 'SQL', 'Git', 'HTML/CSS'],
        'Data Analyst': ['Python', 'SQL', 'Excel','Data Visualization'],
        'UI/UX Designer': ['Figma', 'Adobe XD', 'User Research', 'HTML/CSS'],
        'Mobile Developer': ['Java', 'Kotlin',  'API Integration'],
        'DevOps Engineer': ['Linux', 'Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Python', 'Git'],
    }
    
    if request.method == 'POST':
        target_role = request.POST.get('target_role')
        user_skills_input = request.POST.get('user_skills', '')
        user_skills = [skill.strip() for skill in user_skills_input.split(',') if skill.strip()]
        
        if target_role in role_skills:
            required_skills = role_skills[target_role]
            user_skills_lower = [skill.lower() for skill in user_skills]
            required_skills_lower = [skill.lower() for skill in required_skills]
            
            matching_skills = [skill for skill in required_skills if skill.lower() in user_skills_lower]
            missing_skills = [skill for skill in required_skills if skill.lower() not in user_skills_lower]
            
            results = {
                'target_role': target_role,
                'matching_skills': matching_skills,
                'missing_skills': missing_skills,
                'progress_percentage': int((len(matching_skills) / len(required_skills)) * 100) if required_skills else 0,
            }
    
    context = {
        'roles': role_skills.keys(),
        'results': results
    }
    return render(request, 'main/skill.html', context)

def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '07xxxxxxxx'
    amount = amount
    account_reference = 'Industrylink'
    transaction_desc = 'Service Purchase'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def MpesaPayment(request):
    mentors = Mentor.objects.all()
    
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        amount = int(float(request.POST.get('amount')))
        phone_number = request.POST.get('phone_number')
        
        cl = MpesaClient()
        account_reference = 'IndustryLink Payment'
        callback_url = 'https://api.darajambili.com/express-payment'
        
        if payment_type == 'mentor_session':
            mentor_id = request.POST.get('mentor_id')
            try:
                mentor = Mentor.objects.get(id=mentor_id)
                transaction_desc = f'Mentorship with {mentor.full_name}'
                
                # Trigger M-Pesa STK Push
                response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
                
                messages.success(
                    request, 
                    f'Payment of KES {amount} initiated for session with {mentor.full_name}. Check your phone for M-Pesa prompt!'
                )
            except Mentor.DoesNotExist:
                messages.error(request, 'Selected mentor not found.')
                
        elif payment_type == 'tip_student':
            transaction_desc = 'Student Project Tip'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            messages.success(request, f'Tip of KES {amount} sent successfully!')
            
        elif payment_type == 'donation':
            transaction_desc = 'IndustryLink Donation'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            messages.success(request, f'Thank you for your donation of KES {amount}!')
        
        return redirect('main:payment')
    
    context = {'mentors': mentors}
    return render(request, 'main/payment.html', context)
                                                    


