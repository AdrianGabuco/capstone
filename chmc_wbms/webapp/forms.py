from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    middle_initial = forms.CharField(max_length=1, required=False)
    prefix = forms.ChoiceField(
        choices=[('', 'Select Prefix'), ('Dr.', 'Dr.'), ('Dra.', 'Dra.')],
        required=False
    )
    is_employee = forms.BooleanField(required=False)
    is_associated_doctor = forms.BooleanField(required=False)
    mobile_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'middle_initial', 'prefix', 'mobile_number', 'password', 'confirm_password', 'image','is_employee','is_associated_doctor']

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
    
class CustomUserForm(forms.ModelForm):
    prefix = forms.ChoiceField(
        choices=[('', 'Select Prefix'), ('Dr.', 'Dr.'), ('Dra.', 'Dra.')],
        required=False
    )
    change_password = forms.BooleanField(required=False, label="Change Password")

    # Password fields
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput, label="Confirm Password")


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'prefix', 'is_employee', 'is_associated_doctor', 'image','password','confirm_password','change_password' ]

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
    
class EditProfileForm(forms.ModelForm):
    prefix = forms.ChoiceField(
        choices=[('', 'Select Prefix'), ('Dr.', 'Dr.'), ('Dra.', 'Dra.')],
        required=False
    )
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput, label="Confirm Password")
    change_password = forms.BooleanField(required=False, label="Change Password")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'prefix', 'image', 'password', 'confirm_password','change_password']

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