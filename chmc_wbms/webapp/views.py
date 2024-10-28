from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Sum, Count
from webapp.models import Appointment, Patient, Payment
from django.utils import timezone
from datetime import timedelta

def employee_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type (admin or normal user)
                if user.is_superuser:
                    return redirect('admin_dashboard')  # Change this to your admin dashboard URL
                else:
                    return redirect('home')  # Change this to your normal dashboard URL
    else:
        form = AuthenticationForm()

    return render(request, 'employee/employee_login.html', {'form': form})

def admin_login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:  # Check if the user is an admin
            login(request, user)
            return redirect('admin_dashboard')  # Change to your admin dashboard view
        else:
            form.add_error(None, "You are not authorized to access this page.")

    return render(request, 'admin/admin_login.html', {'form': form})

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