from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! Now you can login!')
            return redirect('login')
        else:
            messages.warning(request,'Unable to create account.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form, 'title':'Student Registration'})

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'Student Profile'})