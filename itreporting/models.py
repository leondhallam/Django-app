from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.models import User, Group

class Issue(models.Model):
    type = models.CharField(max_length=100, choices = [('Hardware', 'Hardware'), ('Software', 'Software')])
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default = False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(User, related_name = 'issues', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.type} Issue in {self.room}'
    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs = {'pk': self.pk})


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(validators=[EmailValidator()], max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at}"

# Module Model
class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)
    credit = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    courses_allowed = models.ManyToManyField(Group, related_name='modules')

    def __str__(self):
        return f"{self.name} ({self.code})"

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile') # Linking the User and Student models
    date_of_birth = models.DateField()
    address = models.TextField()
    city_town = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Registration Model
class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='registrations')
    date_of_registration = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student.user.username} -> {self.module.name}"