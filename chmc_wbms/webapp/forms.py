from django import forms
from .models import CustomUser, Appointment, ServiceType, Patient, Examination, Payment
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models import Q


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'middle_initial',
            'prefix',
            'mobile_number',
            'password',
            'confirm_password',
            'image',
            'is_employee',
            'is_associated_doctor',
            'is_clinic_doctor',
            'signature_image',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'middle_initial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter middle initial (optional)'
            }),
            'prefix': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }),
            'confirm_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'signature_image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'style': 'display: none;'  # Initially hidden
            }),
            'is_employee': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_associated_doctor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_clinic_doctor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        is_associated_doctor = cleaned_data.get('is_associated_doctor')
        is_clinic_doctor = cleaned_data.get('is_clinic_doctor')
        signature_image = cleaned_data.get('signature_image')

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Require signature for doctors
        if (is_associated_doctor or is_clinic_doctor) and not signature_image:
            raise forms.ValidationError("Signature image is required for associated and clinic doctors.")

        # Check for multiple clinic doctors
        if is_clinic_doctor and CustomUser.objects.filter(is_clinic_doctor=True).exists():
            raise forms.ValidationError("A clinic doctor already exists. You cannot create another clinic doctor account.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'middle_initial', 'prefix', 'mobile_number', 'image']
    


class EditAccountForm(forms.ModelForm):
    prefix = forms.ChoiceField(
        choices=CustomUser.PREFIX_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    change_password = forms.BooleanField(
        required=False,
        label="Change Password",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # Password fields
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password (if changing)'
        }),
        label="Password"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label="Confirm Password"
    )

    # Signature field for Associated or Clinic Doctor
    signature_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label="Signature"
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'prefix', 
            'is_employee', 
            'is_associated_doctor', 
            'is_clinic_doctor', 
            'image', 
            'signature_image',  # Added signature field
            'password', 
            'confirm_password', 
            'change_password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'is_employee': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_associated_doctor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_clinic_doctor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial password value only if it’s an update form
        if self.instance.pk:
            self.fields['password'].initial = self.instance.password

            # If the user is an associated or clinic doctor, show the current signature
            if self.instance.is_associated_doctor or self.instance.is_clinic_doctor:
                self.fields['signature_image'].initial = self.instance.signature_image

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        change_password = cleaned_data.get("change_password")

        # Only validate the password if the "Change Password" checkbox is checked
        if change_password:
            if not password:
                self.add_error('password', "Password is required if you want to change it.")
            if not confirm_password:
                self.add_error('confirm_password', "Please confirm the password.")
            elif password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        else:
            # Keep the existing password if "Change Password" is not checked
            cleaned_data['password'] = self.instance.password
            cleaned_data['confirm_password'] = self.instance.password

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)

        # If the "Change Password" checkbox is checked and a password is provided, hash and save the password
        if self.cleaned_data.get('change_password') and self.cleaned_data.get('password'):
            user.password = make_password(self.cleaned_data['password'])
        # If "Change Password" is not checked, keep the current password (don't modify it)
        elif not self.cleaned_data.get('change_password'):
            current_password = user.password  # Keep the existing password
            user.password = current_password  # Reassign it to the user object to prevent being overwritten

        if commit:
            user.save()
        return user
    
class EditProfileForm(forms.ModelForm):
    prefix = forms.ChoiceField(
        choices=CustomUser.PREFIX_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password (if changing)'
        }),
        label="Password"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label="Confirm Password"
    )
    change_password = forms.BooleanField(
        required=False,
        label="Change Password",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'prefix', 'image', 'password', 'confirm_password', 'change_password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial password value only if it’s an update form
        if self.instance.pk:
            self.fields['password'].initial = self.instance.password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        change_password = cleaned_data.get("change_password")

        # Only validate the password if the "Change Password" checkbox is checked
        if change_password:
            if not password:
                self.add_error('password', "Password is required if you want to change it.")
            if not confirm_password:
                self.add_error('confirm_password', "Please confirm the password.")
            elif password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        else:
            # Keep the existing password if "Change Password" is not checked
            cleaned_data['password'] = self.instance.password
            cleaned_data['confirm_password'] = self.instance.password

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # If the "Change Password" checkbox is checked and a password is provided, hash and save the password
        if self.cleaned_data.get('change_password') and self.cleaned_data.get('password'):
            user.password = make_password(self.cleaned_data['password'])
        # If "Change Password" is not checked, keep the current password (don't modify it)
        elif not self.cleaned_data.get('change_password'):
            # Ensure the password is not cleared out if it is not being changed
            current_password = user.password  # Keep the existing password
            user.password = current_password  # Reassign it to the user object to prevent being overwritten

        if commit:
            user.save()
        return user
    
class AppointmentForm(forms.ModelForm):
    service_types = forms.ModelMultipleChoiceField(
        queryset=ServiceType.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Allows multiple selections using checkboxes
        required=True
    )

    class Meta:
        model = Appointment
        fields = ['client_name', 'description', 'service_types', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ExaminationForm(forms.Form):
    # Patient fields
    first_name = forms.CharField(
        max_length=100, 
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first-name'})
    )
    last_name = forms.CharField(
        max_length=100, 
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last-name'})
    )
    middle_name = forms.CharField(
        max_length=100, 
        required=False,
        label="Middle Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'middle-name'})
    )
    age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'age'})
    )
    sex = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')], 
        label="Sex",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'sex'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'id': 'address'}), 
        label="Address",

    )
    contact_number = forms.CharField(
        max_length=15, 
        label="Contact Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'contact-number'})
    )
    image = forms.CharField(required=False, label="Capture Patient Image")  # Field remains the same in the backend

    # Examination fields
    service_types = forms.ModelMultipleChoiceField(
        queryset=ServiceType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Service Types"
    )
    attending_doctor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(Q(is_associated_doctor=True) | Q(is_clinic_doctor=True)),
        label="Attending Doctor"
    )

    # Payment fields
    method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHODS,
        widget=forms.RadioSelect,
        label="Payment Method"
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
    status = forms.ChoiceField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], label="Payment Status")

class UploadEditedDocumentForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = ['edited_document']
        
class UploadResultImageForm(forms.ModelForm):
    result_image_base64 = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Examination
        fields = ['result_image_base64']




class EditExaminationForm(forms.ModelForm):
    # Patient fields
    patient_first_name = forms.CharField(max_length=100, required=False, label="First Name")
    patient_middle_name = forms.CharField(max_length=100, required=False, label="Middle Name")
    patient_last_name = forms.CharField(max_length=100, required=False, label="Last Name")

    # Service types (multiple checkboxes)
    service_types = forms.ModelMultipleChoiceField(
        queryset=ServiceType.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Type of Service"
    )

    # Payment fields
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHODS,
        required=False,
        label="Payment Method"
    )
    payment_status = forms.ChoiceField(
        choices=[('Paid', 'Paid'), ('Pending', 'Pending')],
        required=False,
        label="Payment Status"
    )
    payment_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, label="Payment Amount"
    )

    class Meta:
        model = Examination
        fields = ['service_types']