from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.conf import settings

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
    

class ServiceType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='patient_images/', blank=True, null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Returns full name

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
    is_clinic_doctor = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='../static/image/profile_ICON.png')
    signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Make sure `username` is not required

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"
    

    
class Appointment(models.Model):
    client_name = models.CharField(max_length=100, default="Client")
    description = models.TextField()
    service_types = models.ManyToManyField(ServiceType, through='AppointmentServiceType')
    appointment_date = models.DateField(default=timezone.now)
    appointment_time = models.TimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.client_name} on {self.appointment_date}"

class AppointmentServiceType(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment} - {self.service_type}"
    
    
class Examination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations', default=1)
    service_types = models.ManyToManyField(ServiceType)
    attending_doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Examination for {self.patient}"
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
    ]
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    date = models.DateTimeField(default=timezone.now)  # Date of payment
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')  # Payment method
    status = models.CharField(max_length=100, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')

    def __str__(self):
        return f"{self.examination.id} - {self.amount} via {self.get_method_display()}"