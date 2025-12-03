from django.urls import path
from . import views
path('', views.home, name='home')