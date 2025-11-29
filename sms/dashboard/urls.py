from django.urls import path
from . import views
from .school_view import school_list, school_create, school_update, school_delete  
from .subscription_view import subscription_list, subscription_create, subscription_update, subscription_delete  

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('school/', school_list, name='school_list'),  
    path('school/add/', school_create, name='school_create'),  
    path('school/edit/<int:pk>/', school_update, name='school_update'),  
    path('school/delete/<int:pk>/', school_delete, name='school_delete'),
    path('subscription/', subscription_list, name='subscription_list'),
    path('school/approve/<int:school_id>/', views.accept_school_subscription, name='accept_school_subscription'),
    path('admin/school/<int:school_id>/', views.school_detail_view, name='school_detail'),
    path('subscription/add/', subscription_create, name='subscription_create'),
    path('subscription/edit/<int:pk>/', subscription_update, name='subscription_update'),
    path('subscription/delete/<int:pk>/', subscription_delete, name='subscription_delete'),
]
