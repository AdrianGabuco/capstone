from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Set a default username if one isn't provided
        extra_fields.setdefault('username', email)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):

    PREFIX_CHOICES = [
        ("", "No Prefix"),  # Blank option for no prefix
        ("Dr.", "Dr."),
        ("Dra.", "Dra."),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    prefix = models.CharField(max_length=10, blank=True, null=True, choices=PREFIX_CHOICES)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    is_employee = models.BooleanField(default=False)
    is_associated_doctor = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='../static/image/profile_ICON.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Make sure `username` is not required

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"