from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
# Create your models here.
