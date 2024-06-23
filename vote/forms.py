from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Election, Voter, Candidate, ControlVote
from django import forms
from .models import Profile, Election, Voter, Candidate, ControlVote
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
import uuid

def generate_unique_voter_id():
    return str(uuid.uuid4())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'university_name', 'high_school_name', 'level', 'major', 'student_id', 'district', 'county', 'citizenship', 'age', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'})
        }

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['name', 'start_time', 'end_time', 'max_voters']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Select start time'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Select end time'}),
            'max_voters': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter maximum number of voters'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time.")
        return cleaned_data

class VoterForm(forms.ModelForm):
    voter_id = forms.CharField(max_length=50, required=True, label="Voter ID")

    class Meta:
        model = Voter
        fields = ['election', 'voter_id']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VoterForm, self).__init__(*args, **kwargs)
        if user and user.profile.role == 'commissioner':
            self.fields['election'].queryset = Election.objects.filter(commissioner=user)
            self.fields['election'].label_from_instance = lambda obj: obj.name
            self.fields['election'].widget.attrs['class'] = 'form-control'
        self.fields['voter_id'].widget.attrs['class'] = 'form-control'

def clean_voter_id(self):
    voter_id = self.cleaned_data.get('voter_id')
    if not Voter.objects.filter(voter_id=voter_id, user__isnull=True).exists():
        # Generate a unique voter ID if the provided ID is not valid
        voter_id = generate_unique_voter_id()
        self.cleaned_data['voter_id'] = voter_id  # Update the cleaned data with the generated voter ID
    return voter_id







class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['election', 'position', 'name', 'about', 'party', 'image']
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'party': forms.Select(attrs={'class': 'form-control'}),
        }

class ControlVoteForm(forms.ModelForm):
    class Meta:
        model = ControlVote
        fields = ['user', 'position', 'election', 'candidate', 'party', 'status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'election': forms.Select(attrs={'class': 'form-control'}),
            'candidate': forms.Select(attrs={'class': 'form-control'}),
            'party': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    university_name = forms.CharField(max_length=100, required=False)
    high_school_name = forms.CharField(max_length=100, required=False)
    level = forms.CharField(max_length=50, required=False)
    major = forms.CharField(max_length=100, required=False)
    student_id = forms.CharField(max_length=50, required=False)
    district = forms.CharField(max_length=50, required=True)
    county = forms.CharField(max_length=50, required=True)
    citizenship = forms.BooleanField(required=False, initial=False)
    age = forms.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)])
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    voter_id = forms.CharField(max_length=50, required=False, label="Voter ID")
    terms_of_service = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the Terms of Service.'}
    )
    privacy_policy = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the Privacy Policy.'}
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 
            'university_name', 'high_school_name', 'level', 'major', 'student_id', 
            'district', 'county', 'citizenship', 'age', 'role', 'voter_id', 'terms_of_service', 'privacy_policy'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_voter_id(self):
        role = self.cleaned_data.get('role')
        voter_id = self.cleaned_data.get('voter_id')
        if role == 'voter':
            if not voter_id:
                raise forms.ValidationError("Voter ID is required for voters.")
            if not Voter.objects.filter(voter_id=voter_id, user__isnull=True).exists():
                raise forms.ValidationError("Invalid or already used Voter ID.")
        return voter_id

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'commissioner':
            cleaned_data['voter_id'] = ''  # Clear voter_id field if role is commissioner
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = Profile(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                university_name=self.cleaned_data['university_name'],
                high_school_name=self.cleaned_data['high_school_name'],
                level=self.cleaned_data['level'],
                major=self.cleaned_data['major'],
                student_id=self.cleaned_data['student_id'],
                district=self.cleaned_data['district'],
                county=self.cleaned_data['county'],
                citizenship=self.cleaned_data['citizenship'],
                age=self.cleaned_data['age'],
                role=self.cleaned_data['role']
            )
            profile.save()

        return user





class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('university_name', 'high_school_name', 'level', 'major', 'student_id', 'district', 'county', 'citizenship', 'age')
        widgets = {
            'university_name': forms.TextInput(attrs={'class': 'form-control'}),
            'high_school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
