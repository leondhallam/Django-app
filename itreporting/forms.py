# from django import forms
# from .models import Contact

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'subject', 'message', 'address']

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div, Row, Column
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    subject = forms.CharField(max_length=100, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")

# class ContactForm(forms.Form):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'subject', 'message', 'address']

#     name = forms.CharField(max_length=100, label="Name", help_text="Enter your full name.")
#     email = forms.EmailField(label="Email address", help_text="We will reply to this email.")
#     message = forms.CharField(widget=forms.Textarea, label="Message", help_text="Your message or query.")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.form_action = '/contact/'  # Action URL for form submission
#         self.helper.layout = Layout(
#             Row(
#                 Column(Field('name', css_class='form-control'), css_class='col-md-6'),
#                 Column(Field('email', css_class='form-control'), css_class='col-md-6'),
#             ),
#             Field('message', css_class='form-control'),
#             Submit('submit', 'Submit', css_class='btn btn-primary w-100 mt-3')  # Full-width button
#         )

