from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.updateProfile, name='updateProfile'),
    path('login/', views.loginHome, name='login'),
    path('register/', views.registerHome, name='register'),
    path('home/school/register/', views.registerSchool, name='school_register'),
    path('home/schools/', views.home_school_list, name='home_school_list'),
    path('home/schools/<int:pk>/', views.home_school_detail, name='home_school_detail'), 
     path('home/school/<int:pk>/apply/', views.apply_to_school, name='home_submit_application'),
]
