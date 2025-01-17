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
from webapp.views import edit_examination, upload_examination_result_image, search_patient, verify_document, employee_examination_view,download_document, upload_edited_document, view_document, employee_login_view, admin_login_view, admin_dashboard_view, admin_logout_view, create_account_view, employee_dashboard_view, patients_list_view, manage_account_view, edit_account_view, delete_account_view, employee_logout_view, edit_profile_view, employee_patients_list_view, assoc_doc_readings_view, associated_doctors_view, document_results_view, add_examination
from django.conf.urls.static import static
from django.conf import settings
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', employee_login_view, name='employee_login'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('manage_accounts/', manage_account_view, name='manage_accounts'),
    path('patients_list/', patients_list_view, name='patients_list'),
    path('employee_dashboard/', employee_dashboard_view, name='employee_dashboard'),
    path('create_account/', create_account_view, name='create_account'),
    path('logout/', admin_logout_view, name='admin_logout'),
    path('employee_logout/', employee_logout_view, name='employee_logout'),
    path('edit_account/<int:account_id>/', edit_account_view, name='edit_account'),
    path('delete_account/<int:account_id>/', delete_account_view, name='delete_account'),
    path('edit_profile/<int:account_id>/', edit_profile_view, name='edit_profile'),
    path('employee_patients_list/', employee_patients_list_view, name='employee_patients_list'),
    path('assoc_doc_readings', assoc_doc_readings_view, name='assoc_doc_readings'),
    path('associated_doctors/', associated_doctors_view, name='associated_doctors'),
    path('document_results/', document_results_view, name='document_results'),
    path('employee_examination/', employee_examination_view, name='employee_examination'),
    path('add_examination/', add_examination, name='add_examination'),
    path('examination/<int:pk>/upload/', upload_edited_document, name='upload_edited_document'),
    path('examination/<int:pk>/view/', view_document, name='view_document'),
    path('verify-document/', verify_document, name='verify_document'),
    path('search_patient/', search_patient, name='search_patient'),
    path('upload-result-image/<int:pk>/', upload_examination_result_image, name='upload_examination_result_image'),
    path('edit-examination/<int:pk>/', edit_examination, name='edit_examination'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)