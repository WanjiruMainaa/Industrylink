from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProjectForm, ProfileEditForm
from .models import StudentProfile, Project, Mentor


# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(
                user=user,
                institution=form.cleaned_data['institution'],
                course=form.cleaned_data['course'],
                year_of_study=form.cleaned_data['year_of_study'],
                email=form.cleaned_data['email']
            )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('main:login')
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, 'main/register.html', context)

       

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist!")
            return render(request, 'main/login.html')
        
        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return redirect('main:dashboard')
        else:
            messages.error("Incorrect username or password")
    
    context ={}
    return render(request, 'main/login.html',context )


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
        'skills': skill,
    }
    return render(request, 'main/dashboard.html', context)

def projects_list(request):
    all_projects = Project.objects.all()
    return render(request, 'main/projects.html', {'projects': all_projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = StudentProfile.objects.get(user=request.user)
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('main:dashboard')
    else:
        form = ProjectForm()

    return render(request, 'main/projects.html', {'form': form})

@login_required(login_url='main:login')
def edit_profile(request):
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
    
    return render(request, 'main/edit_profile.html', {'form': form})

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
                                                    


