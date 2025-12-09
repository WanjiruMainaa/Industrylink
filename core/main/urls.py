from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('mentor/', views.mentor_list, name='mentor'),
    path('skill_gap/', views.skill_gap_analyser, name='skills'),
    path('profile/edit/', views.editProfile, name='editProfile'),
    path('index/', views.index, name='index'),
    path('payment/', views.MpesaPayment, name='payment'),
    path('projects/mark-complete/<int:project_id>/', views.mark_project_complete, name='mark_complete'),
    path('projects/review/<int:project_id>/', views.review_project, name='review_project'),
]
