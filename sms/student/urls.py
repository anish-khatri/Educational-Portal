from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('profile/', views.profile, name='student_profile'),
    path('update-profile/', views.updateProfile, name='student_updateProfile'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/edit/<int:application_id>/', views.edit_application, name='edit_application'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('applications/show/<int:application_id>/', views.show_application, name='show_application'),
    path('applications/<int:application_id>/results/', views.result_list, name='student_result_list'),
    path('application/full_data/<int:application_id>/', views.show_application_full_data, name='show_application_full_data'),
    path('result/<int:result_id>/', views.show_result, name='show_result'),
    path('result/<int:result_id>/download/', views.download_result_pdf, name='download_result_pdf'),
    
    path('admission/create/<int:application_id>/',views.admission_create, name='admission_create'),
    path('admissions/', views.admission_list, name='admission_list'),
    path('admissions/<int:admission_id>/', views.admission_detail, name='admission_detail'),
    path("payment/<int:admission_id>/", views.payment_form, name="payment_form"),
    path("payment/success/<str:transaction_id>/", views.esewa_payment_success, name="esewa_payment_success"),
    path("payment/failure/<str:transaction_id>/", views.esewa_payment_failure, name="esewa_payment_failure"),
    path('notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]

handler404 = 'student.views.custom_404'