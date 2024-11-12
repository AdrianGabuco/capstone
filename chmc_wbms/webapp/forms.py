from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    middle_initial = forms.CharField(max_length=1, required=False)
    prefix = forms.ChoiceField(
        choices=[('', 'Select Prefix'), ('Dr.', 'Dr.'), ('Dra.', 'Dra.')],
        required=False
    )
    account_type = forms.ChoiceField(choices=[('employee', 'Employee'), ('doctor', 'Associated Doctor')])
    mobile_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data