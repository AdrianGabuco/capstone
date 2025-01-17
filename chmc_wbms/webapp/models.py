import hashlib
import base64
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.conf import settings
from tinymce.models import HTMLField
from django.core.files.base import ContentFile


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
    
    def get_full_name_with_middle_initial(self):
        middle_initial = f"{self.middle_name[0].upper()}." if self.middle_name else ""
        full_name = f"{self.first_name} {middle_initial} {self.last_name}".strip()
        return full_name
    
    def patient_full_name_last_name_start(self):
        middle_initial = f"{self.middle_name[0].upper()}." if self.middle_name else ""
        full_name = f"{self.last_name}, {self.first_name} {middle_initial}".strip()
        return full_name
    
    def get_formatted_id(self):
    # Determine the required number of digits based on total patient count
        total_patients = Patient.objects.count()
        num_digits = len(str(total_patients)) + 1  # One extra digit to future-proof
        return f"PID-{self.id:0{num_digits}d}"
    def get_secure_hashed_id(self):
        """Return the SHA-256 hash of the formatted ID with salt and pepper."""
        salt = "Patient2025"
        pepper = "Identity2024"
        formatted_id = self.get_formatted_id()
        to_hash = f"{salt}{formatted_id}{pepper}"
        hashed_id = hashlib.sha256(to_hash.encode()).hexdigest()
        return hashed_id

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
    
    def get_full_name_with_middle_initial(self):
        middle_name = f"{self.middle_initial[0].upper()}." if self.middle_initial else ""
        full_name = f"{self.first_name} {middle_name} {self.last_name}".strip()
        return full_name
    

    
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
    document = models.FileField(upload_to='examination_documents/', null=True, blank=True)
    edited_document = models.FileField(upload_to='examination_documents/edited', null=True, blank=True)  # Edited document
    original_document_hash = models.CharField(max_length=64, null=True, blank=True)
    result_image = models.ImageField(upload_to='examination_results/', null=True, blank=True)  # New field for result image

    def calculate_document_hash(self, file_path):
        """Calculate SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def save_original_document_hash(self):
        """Save the hash of the original document."""
        if self.edited_document:
            self.original_document_hash = self.calculate_document_hash(self.edited_document.path)
            self.save()

    def verify_document_integrity(self):
        """Verify if the document has changed by comparing hashes."""
        if not self.edited_document or not self.original_document_hash:
            return False  # Document integrity cannot be verified
        current_hash = self.calculate_document_hash(self.edited_document.path)
        return current_hash == self.original_document_hash

    def has_edited_document(self):
        return bool(self.edited_document)
    def __str__(self):
        return f"Examination for {self.patient}"
    
    def get_file_number(self):
        year_suffix = self.date_created.strftime("%y")  # Get the last two digits of the year
        file_count = Examination.objects.filter(
            date_created__year=self.date_created.year
        ).count() + 1  # Count examinations for the current year and increment by 1
        return f"{year_suffix}-{file_count:02d}"  # Format as '25-01', '25-02', etc.
    
    def get_unique_code(self):
        salt = "CHMC2024"
        pepper = "WBMS2025"
        file_number = self.get_file_number()
        patient_full_name = self.patient.get_full_name_with_middle_initial()
        doctor_full_name = self.attending_doctor.get_full_name_with_middle_initial()
        raw_code = f"{file_number}-{patient_full_name}-{doctor_full_name}"
        sha_input = f"{salt}{raw_code}{pepper}".encode('utf-8')
        unique_code = hashlib.sha256(sha_input).hexdigest()[:8].upper()
        return f"CHMC-{unique_code}"

    # Optional: Full SHA-256 unique code (if needed)
    def get_raw_unique_code(self):
        salt = "CHMC2024"
        pepper = "WBMS2025"
        file_number = self.get_file_number()
        patient_full_name = self.patient.get_full_name_with_middle_initial()
        doctor_full_name = self.attending_doctor.get_full_name_with_middle_initial()
        raw_code = f"{file_number}-{patient_full_name}-{doctor_full_name}"
        sha_input = f"{salt}{raw_code}{pepper}".encode('utf-8')
        return hashlib.sha256(sha_input).hexdigest()
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Gcash', 'GCash'),
    ]
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    date = models.DateTimeField(default=timezone.now)  # Date of payment
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='Cash')  # Payment method
    status = models.CharField(max_length=100, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')

    def __str__(self):
        return f"{self.examination.id} - {self.amount} via {self.get_method_display()}"