from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

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
            'is_associated_doctor'
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
            'is_employee': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_associated_doctor': forms.CheckboxInput(attrs={
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

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

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

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'prefix', 
            'is_employee', 
            'is_associated_doctor', 
            'image', 
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