from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.validators import EmailValidator
from itreporting.models import Contact

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

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'subject', 'message', 'address']