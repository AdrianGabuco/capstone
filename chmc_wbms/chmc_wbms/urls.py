"""
URL configuration for chmc_wbms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import assocdoc_document_results_view, assocdoc_patients_list_view, assocdoc_examination_view,assocdoc_logout_view, assocdoc_edit_profile_view, delete_edited_document_view,delete_patient_view,delete_examination_view, admin_edit_patient,admin_add_examination, admin_document_results_view, admin_examination_view, assocdoc_dashboard_view,edit_patient, edit_examination, upload_examination_result_image, search_patient, verify_document, employee_examination_view, upload_edited_document, view_document, user_login_view, admin_login_view, admin_dashboard_view, admin_logout_view, create_account_view, employee_dashboard_view, patients_list_view, manage_account_view, edit_account_view, delete_account_view, employee_logout_view, edit_profile_view, employee_patients_list_view, document_results_view, add_examination, search_patients_list, get_available_time_slots, get_appointment_details
from django.conf.urls.static import static
from django.conf import settings
    
urlpatterns = [
    #login
    path('', user_login_view, name='user_login'),
    path('admin_login/', admin_login_view, name='admin_login'),
    #Admin
    path('admin/', admin.site.urls),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('manage_accounts/', manage_account_view, name='manage_accounts'),
    path('patients_list/', patients_list_view, name='admin_patients_list'),
    path('admin_patients_list/<int:patient_id>/', patients_list_view, name='admin_patients_list_with_id'),
    path('create_account/', create_account_view, name='create_account'),
    path('logout/', admin_logout_view, name='admin_logout'),
    path('admin_document_results/', admin_document_results_view, name='admin_document_results'),
    path('admin_examination/', admin_examination_view, name='admin_examination'),
    path('admin_add_examination/', admin_add_examination, name='admin_add_examination'),
    path('admin_edit_patient/<int:patient_id>/', admin_edit_patient, name='admin_edit_patient'),
    path('delete-examination/<int:pk>/', delete_examination_view, name='admin_delete_examination'),
    path('delete-patient/<int:pk>/', delete_patient_view, name='admin_delete_patient'),
    path('delete-document/<int:pk>/', delete_edited_document_view, name='delete_edited_document'),

    #Employee
    path('employee_dashboard/', employee_dashboard_view, name='employee_dashboard'), 
    path('employee_logout/', employee_logout_view, name='employee_logout'),
    path('edit_account/<int:account_id>/', edit_account_view, name='edit_account'),
    path('delete_account/<int:account_id>/', delete_account_view, name='delete_account'),
    path('edit_profile/<int:account_id>/', edit_profile_view, name='edit_profile'),

    #Patients_list
    path('employee_patients_list/', employee_patients_list_view, name='employee_patients_list'),
    path('employee_patients_list/<int:patient_id>/', employee_patients_list_view, name='employee_patients_list_with_id'),
    path('edit_patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    path('search-patients/', search_patients_list, name='search_patients_list'), 

    #Document Results
    path('employee_document_results/', document_results_view, name='document_results'),

    #Examination
    path('employee_examination/', employee_examination_view, name='employee_examination'),
    path('add_examination/', add_examination, name='add_examination'),
    path('search_patient/', search_patient, name='search_patient'), #Add Examination Search
    path('examination/<int:pk>/upload/', upload_edited_document, name='upload_edited_document'),
    path('examination/<int:pk>/view/', view_document, name='view_document'),
    path('upload-result-image/<int:pk>/', upload_examination_result_image, name='upload_examination_result_image'),
    path('edit-examination/<int:pk>/', edit_examination, name='edit_examination'),

    #Authenticity Checker
    path('verify-document/', verify_document, name='verify_document'),
    
    #Appointment
    path('get-available-time-slots/', get_available_time_slots, name='get_available_time_slots'),
    path('get-appointment-details/', get_appointment_details, name='get_appointment_details'),

    #Associated Doctor
    path('assocdoc_dashboard/', assocdoc_dashboard_view, name='assocdoc_dashboard'),
    path('assocdoc_edit_profile/<int:account_id>/', assocdoc_edit_profile_view, name='assocdoc_edit_profile'),
    path('assocdoc_logout/', assocdoc_logout_view, name='assocdoc_logout'),
    path('assocdoc_examination/', assocdoc_examination_view, name='assocdoc_examination'),
    path('assocdoc_patients_list/', assocdoc_patients_list_view, name='assocdoc_patients_list'),
    path('assocdoc_patients_list/<int:patient_id>/', assocdoc_patients_list_view, name='assocdoc_patients_list_with_id'),
    path('assocdoc_document_results/', assocdoc_document_results_view, name='assocdoc_document_results'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)