from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):

    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    year_of_study = models.IntegerField() 
    course = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    skills = models.TextField(help_text="Comma-separated skills")
    phone = models.CharField(max_length=15, blank=True) 
    #profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
    
    def __str__(self):
        return f"{self.user.username} - {self.course}"
    

class Skill(models.Model):
    Skill_Level_choices = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    name = models.CharField(max_length=50, unique=True)
    level = models.CharField(max_length=20, choices=Skill_Level_choices, default='beginner')
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
     
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_used = models.TextField()
    #github_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    #live_demo_link = models.URLField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    #image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
class Mentor(models.Model):
    Expertise = [
        ('technology', 'Technology'),
        ('health', 'Health'),
        ('marketing', 'Marketing'),
        ('business', 'Business'),
        ('psychology', 'Psychology'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('design', 'Design'),
        ('law', 'Law'),
        ('other', 'Other'),
    ]
    full_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    expertise_area = models.CharField(max_length=50, choices=Expertise)
    field = models.CharField(max_length=200)
    years_of_experience = models.IntegerField()
    availability = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    bio = models.TextField()
    email = models.EmailField()
    #linkedin = models.URLField(blank=True)
    #profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.field}"
