from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    district = forms.CharField(max_length=50)
    county = forms.CharField(max_length=50)
    national_id = forms.CharField(max_length=50)
    citizenship = forms.BooleanField(required=True)
    age = forms.IntegerField(min_value=18)
    residency_proof = forms.FileField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Additional eligibility checks
        citizenship = cleaned_data.get('citizenship')
        age = cleaned_data.get('age')
        residency_proof = cleaned_data.get('residency_proof')

        if not citizenship:
            raise forms.ValidationError("You must be a citizen to register.")

        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")

        if not residency_proof:
            raise forms.ValidationError("Residency proof is required.")

        # Additional checks as needed

        return cleaned_data

class ChangeForm(forms.ModelForm):
    district = forms.CharField(max_length=50)
    county = forms.CharField(max_length=50)
    national_id = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'district', 'county', 'national_id']
