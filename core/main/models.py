from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('organization', 'Organization'),
        ('freelancer', 'Freelancer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class StudentProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    year_of_study = models.IntegerField() 
    course = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    email = models.EmailField()
    bio = models.TextField(blank=True)
    skills = models.TextField(help_text="Comma-separated skills") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course}"
    

class Skill(models.Model):
    SKILLS_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skill_set', null=True, blank=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=SKILLS_LEVEL_CHOICES, default='beginner')
    years_of_experience = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

   
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Project(models.Model):
     
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ] 
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='projects')
    freelancer = models.ForeignKey('Freelancer', on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_used = models.TextField()
    github_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
class Mentor(models.Model):
    EXPERTISE_CHOICES = [
        ('technology', 'Technology'),
        ('design', 'Design'),
        ('other', 'Other'),
        ('business', 'Business')
    ]
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    full_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    expertise_area = models.CharField(max_length=50, choices=EXPERTISE_CHOICES)
    years_of_experience = models.IntegerField()
    availability = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.job_title}"

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization_profile')
    organization_name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=100, help_text="e.g., NGO, Startup, Corporation")
    industry = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['organization_name']
    
    def __str__(self):
        return f"{self.organization_name} - {self.organization_type}"

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    full_name = models.CharField(max_length=200)
    profession = models.CharField(max_length=200, help_text="e.g., Web Developer, Designer")
    specialization = models.CharField(max_length=200)
    years_of_experience = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    email = models.EmailField()

    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.profession}"