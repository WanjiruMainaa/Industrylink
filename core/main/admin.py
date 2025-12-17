from django.contrib import admin
from .models import (
    StudentProfile, Mentor, Organization, 
    Freelancer, Project
)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'institution', 'year_of_study', 'created_at']
    list_filter = ['year_of_study', 'institution']
    search_fields = ['user__username', 'course', 'institution']

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job_title', 'company', 'expertise_area', 'years_of_experience']
    list_filter = ['expertise_area', 'company']
    search_fields = ['full_name', 'job_title', 'company']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'organization_type', 'industry', 'email']
    list_filter = ['organization_type', 'industry']
    search_fields = ['organization_name', 'industry']

@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'profession', 'specialization', 'years_of_experience']
    list_filter = ['profession']
    search_fields = ['full_name', 'profession', 'specialization']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'status', 'start_date', 'created_at']
    list_filter = ['status', 'start_date']
    search_fields = ['title', 'description', 'student__user__username']
    date_hierarchy = 'created_at'