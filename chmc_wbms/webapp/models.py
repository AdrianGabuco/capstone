from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
    ]

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)  # Reference to the patient
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    date = models.DateTimeField(default=timezone.now)  # Date of payment
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')  # Payment method

    def __str__(self):
        return f"{self.patient.name} - {self.amount} via {self.get_method_display()}"
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.user.username} on {self.date}"


class CustomUser(AbstractUser):
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    is_employee = models.BooleanField(default=False)
    is_associated_doctor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
# Create your models here.
