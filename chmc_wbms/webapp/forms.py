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
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Password")


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'prefix', 'is_employee', 'is_associated_doctor', 'image', 'password']

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user