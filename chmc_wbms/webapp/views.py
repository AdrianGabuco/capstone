from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Sum, Count
from webapp.models import Appointment, Patient, Payment, CustomUser
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta
from .forms import UserCreationForm, CustomUserForm, EditProfileForm
from django.views.decorators.csrf import csrf_protect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Determine user type and redirect accordingly
            if user.is_superuser:  # Assuming superuser is the admin
                return redirect('admin_dashboard')
            elif hasattr(user, 'is_employee') and user.is_employee:
                return redirect('employee_dashboard')
            elif hasattr(user, 'is_associated_doctor') and user.is_associated_doctor:
                return redirect('assoc_doc_dashboard')
            else:
                # Redirect to a default page or show an error
                messages.error(request, "Access not allowed.")
                return redirect('login')  # Replace 'login' with your login page name
        else:
            messages.error(request, "Invalid credentials")
            
    return render(request, 'login.html')

@csrf_protect
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            # Set custom session data (Django manages session storage automatically)
            session_key = f"admin_session_{get_random_string(32)}"
            request.session['session_key'] = session_key
            request.session['user_id'] = user.id
            response = HttpResponseRedirect(reverse('admin_dashboard'))
            response.set_cookie('admin_session', session_key, httponly=True)
            return response
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")
    return render(request, 'admin/admin_login.html')


def employee_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None and hasattr(user, 'is_employee') and user.is_employee:
                login(request, user)
                # Set custom session data (Django manages session storage automatically)

                response = HttpResponseRedirect(reverse('employee_dashboard'))

                return response
            else:
                messages.error(request, "Invalid credentials or unauthorized access.")
    else:
        form = AuthenticationForm()

    return render(request, 'employee/employee_login.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def manage_account_view(request):
    # Filter out the superuser accounts and get only employees and associated doctors
    accounts = CustomUser.objects.exclude(is_superuser=True).filter(is_employee=True) | CustomUser.objects.exclude(is_superuser=True).filter(is_associated_doctor=True)

    # Context to pass to the template
    context = {
        'accounts': accounts,
    }
    return render(request, 'admin/manage_accounts.html', context)

@user_passes_test(lambda u: u.is_superuser)
def patients_list_view(request):
    return render(request, 'admin/patients_list.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard_view(request):
    # today = timezone.now()
    # start_of_week = today - timedelta(days=today.weekday())

    # # Total income by payment method
    # daily_income_cash = Payment.objects.filter(date__date=today.date(), method='cash').aggregate(total=Sum('amount'))['total'] or 0
    # daily_income_gcash = Payment.objects.filter(date__date=today.date(), method='gcash').aggregate(total=Sum('amount'))['total'] or 0
    # weekly_income_cash = Payment.objects.filter(date__gte=start_of_week, method='cash').aggregate(total=Sum('amount'))['total'] or 0
    # weekly_income_gcash = Payment.objects.filter(date__gte=start_of_week, method='gcash').aggregate(total=Sum('amount'))['total'] or 0

    # # Count total patients attended
    # # Count total patients for today
    # today_patients = Patient.objects.count

    # # Count total patients for the week
    # weekly_patients = Patient.objects.count

    # # Get today's appointments
    # today_appointments = Appointment.objects.filter(date__date=today.date())
    
    # # Get all appointments
    # all_appointments = Appointment.objects.all()

    # context = {
    #     'daily_income_cash': daily_income_cash,
    #     'daily_income_gcash': daily_income_gcash,
    #     'weekly_income_cash': weekly_income_cash,
    #     'weekly_income_gcash': weekly_income_gcash,
    #     'today_patients': today_patients,  # Total distinct patients today
    #     'weekly_patients': weekly_patients,  # Total distinct patients this week
    #     'today_appointments': today_appointments,  # Today's appointments
    #     'all_appointments': all_appointments,  # All appointments
    # }

    return render(request, 'admin/admin_dashboard.html')

def admin_logout_view(request):
    logout(request)  # This logs out the user
    return redirect('admin_login') 

def employee_logout_view(request):
    logout(request)  # This logs out the user
    return redirect('employee_login') 


def create_account_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.password = make_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            
            # Save the user to database
            user.save()

            # Add additional fields to user profile

            account_type = request.POST.get('account_type')  # Get the selected account type
            if account_type == 'employee':
                user.is_employee = True
            elif account_type == 'assoc_doctor':
                user.is_associated_doctor = True


            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error creating account. Please check the details.")

    else:
        form = UserCreationForm()
    return render(request, 'admin/create_account.html', {'form': form})

@user_passes_test(lambda u: u.is_employee)
def employee_dashboard_view(request):
       account = request.user
       context = {'account': account}
       return render(request, 'employee/employee_dashboard.html', context)

@login_required
def edit_account_view(request, account_id):
    account = get_object_or_404(CustomUser, id=account_id)
    form = CustomUserForm(request.POST or None, request.FILES or None, instance=account)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('manage_accounts')
        else:
            messages.error(request, 'Please correct the error below.')
    
    return render(request, 'admin/edit_account.html', {'form': form, 'account': account})

@login_required
def delete_account_view(request, account_id):
    account = get_object_or_404(CustomUser, id=account_id)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('manage_accounts')
    
    return render(request, 'admin/delete_account.html', {'account': account})

@login_required
def edit_profile_view(request, account_id):
    account = get_object_or_404(CustomUser, id=account_id)
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=account)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('employee_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    
    return render(request, 'employee/edit_profile.html', {'form': form, 'account': account})


@user_passes_test(lambda u: u.is_employee)
def employee_patients_list_view(request):
       account = request.user
       context = {'account': account}
       return render(request, 'employee/patients_list.html', context)


@user_passes_test(lambda u: u.is_employee)
def document_results_view(request):
       account = request.user
       context = {'account': account}
       return render(request, 'employee/document_results.html', context)


@user_passes_test(lambda u: u.is_employee)
def assoc_doc_readings_view(request):
       account = request.user
       context = {'account': account}
       return render(request, 'employee/assoc_doc_readings.html', context)

@user_passes_test(lambda u: u.is_employee)
def associated_doctors_view(request):
       account = request.user
       context = {'account': account}
       return render(request, 'employee/associated_doctors.html', context)


