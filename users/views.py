from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from itreporting.models import Student
from .forms import UserRegistrationForm, StudentRegistrationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            course = student_form.cleaned_data.get('course')
            if course:
                user.groups.add(course)

            messages.success(request, 'Your account has been created! Now you can log in.')
            return redirect('login')
        else:
            messages.warning(request, 'Unable to create account. Please check the form.')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentRegistrationForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'student_form': student_form,
        'title': 'Student Registration'
    })

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentRegistrationForm(request.POST, request.FILES, instance=request.user.student_profile)
        p_form.fields['course'].initial = request.user.groups.first()

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save(user=request.user)
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentRegistrationForm(instance=request.user.student_profile)
        p_form.fields['course'].initial = request.user.groups.first()

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)

