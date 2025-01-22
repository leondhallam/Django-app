from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
import requests
from .forms import ContactForm
from .models import ContactSubmission, Module, ModuleRegistration
from django.core.mail import EmailMessage
from django.contrib import messages


def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = 'd3da844b10cd6d5411c2c9e0a694e8e7'

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json() # Request the API data and convert the JSON to Python data types

        weather = {
            'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description']
        }   
        weather_data.append(weather) # Add the data for the current city into our list
    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the submission to the database
            # ContactSubmission.objects.create(
            #     name=form.cleaned_data['name'],
            #     email=form.cleaned_data['email'],
            #     subject=form.cleaned_data['subject'],
            #     message=form.cleaned_data['message']
            # )
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject=form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_subject = '{} - Contact Form Submission from {}'.format(subject, name)

            EmailMessage(
                email_subject,
                #'Contact Form Submission from {}'.format(name),
                message,
                'form-response@example.com',
                ['c2012047@my.shu.ac.uk'],
                [],
                reply_to=[email]
            ).send()
            return HttpResponse('Success!')
    else:
        form = ContactForm()

    return render(request, 'itreporting/contact.html', {'form': form, 'title': 'Contact Us'})

# def success(request):
#     return HttpResponse('Success!')


def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About Us'})

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

def modules(request):
    modules = Module.objects.all()

    context = {
        'modules': modules,
    }

    return render(request, 'itreporting/modules.html', context)

@login_required
def module_detail(request, module_id):
    module = Module.objects.get(id=module_id)
    student_profile = request.user.student_profile

    # Check if the student is registered for this module already
    is_registered = student_profile.modules.filter(id=module.id).exists()

    # Check if the student’s course is allowed to register for this module
    if request.method == 'POST':
        if module.courses_allowed.filter(id=student_profile.course.id).exists():
            if is_registered:
                # Unregister if already registered
                student_profile.modules.remove(module)
                messages.success(request, f'You have unregistered from {module.name}.')
            else:
                # Register if not already registered
                student_profile.modules.add(module)
                messages.success(request, f'You have registered for {module.name}.')
        else:
            messages.error(request, 'You cannot register for this module because it is not available for your course.')

    context = {
        'module': module,
        'is_registered': is_registered,
    }
    return render(request, 'itreporting/module_detail.html', context)




class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5 # Optional pagination

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

