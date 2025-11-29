from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='school_dashboard'),
    path('profile/', views.profile, name='school_profile'),
    path('update-profile/', views.updateProfile, name='school_updateProfile'),
    path('applications/', views.application_list, name='application_list'),
    path('approved-applications/', views.approved_application_list, name='approved_application_list'),
    path('waiting-applications/', views.waiting_application_list, name='waiting_application_list'),
    path('applications/show/<int:application_id>/', views.show_application, name='school_show_application'),
    path('convert_waiting_exam/<int:application_id>/', views.convert_waiting_exam, name='convert_waiting_exam'),
    path('create_student_entrance_exam/<int:application_id>/', views.create_student_entrance_exam, name='create_student_entrance_exam'),
    path('publish_result/<int:application_id>/', views.publish_result, name='publish_result'),
    path('applications/<int:application_id>/results/', views.result_list, name='result_list'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('create/', views.create_course, name='create_course'),
    path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('admissions/', views.admission_list, name='school_admission_list'),
    path('admissions/<int:admission_id>/', views.admission_detail, name='school_admission_detail'),
]
