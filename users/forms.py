from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.validators import EmailValidator
from itreporting.models import Student
from datetime import datetime

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class StudentRegistrationForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    date_of_birth = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'}),
        help_text="Enter your date of birth in DD/MM/YYYY format."
    )
    course = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label="Select a course",
        help_text="Select the course you're studying."
    )

    class Meta:
        model = Student
        fields = ['date_of_birth', 'address', 'city_town', 'country', 'photo']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > datetime.today().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth

    def save(self, user, commit=True):
        student = super().save(commit=False)
        student.user = user

        if commit:
            student.save()

        course = self.cleaned_data.get('course')
        if course:
            user.groups.clear()
            user.groups.add(course)

        return student