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
    course = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label="Select a course",
        help_text="Select the course you're studying."
    )
    date_of_birth = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'}),
        help_text="Enter your date of birth in DD/MM/YYYY format."
    )

    class Meta:
        model = Student
        fields = ['date_of_birth', 'address', 'city_town', 'country', 'photo', 'course']  # Include 'course' field in Meta

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > datetime.today().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth

    def save(self, user=None, commit=True):
        # Save the student profile
        student = super().save(commit=False)
        
        if user:
            student.user = user  # Associate the student profile with the user

        if commit:
            student.save()

        # Save the course (only if it's selected)
        course = self.cleaned_data.get('course')
        if course:
            student.course = course  # Assign course to student profile
            student.save()

            # Also update the user’s groups (course)
            user.groups.clear()  # Remove any existing course associations
            user.groups.add(course)  # Add the new course

        return student

