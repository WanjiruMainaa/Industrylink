from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('projects/', views.projects, name='projects'),
    path('mentors/', views.mentor_list, name='mentor'),
    path('skills/', views.skill_gap_analyser, name='skills'),
    path('payment/', views.MpesaPayment, name='payment'),
    
    # Authentication
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    # Dashboard (One dynamic dashboard for all users)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile CRUD
    path('profile/edit/', views.editProfile, name='editProfile'),
    
    # Project CRUD Operations
    path('project/add/', views.add_project, name='add_project'),
    path('project/<int:project_id>/', views.view_project, name='view_project'), 
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'), 
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),  
]