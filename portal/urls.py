from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('register/company/', views.register_company, name='register_company'),
    path('job/new/', views.create_job, name='create_job'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/edit/', views.update_job, name='update_job'),
    path('job/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/applicants/', views.applicant_list, name='applicant_list'),
    path('application/<int:app_id>/status/<str:status>/', views.update_application_status, name='update_status'),
    path('my-applications/', views.my_applications, name='my_applications'),
]
