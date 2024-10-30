from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'Contact Us'})

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About Us'})
