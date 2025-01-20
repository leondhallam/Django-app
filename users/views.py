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
            # Save the user first
            user = user_form.save()
            
            # Save the student profile and associate it with the user
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            # Assign the selected course (Group) to the user
            course = student_form.cleaned_data.get('course')
            if course:
                user.groups.clear()  # Clear any previous groups
                user.groups.add(course)  # Add the selected course

            # Notify the user of successful registration
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
    if hasattr(request.user, 'student_profile'):
        p_form = StudentRegistrationForm(request.POST, request.FILES, instance=request.user.student_profile)
    else:
        p_form = StudentRegistrationForm(request.POST, request.FILES)

    u_form = UserUpdateForm(request.POST, instance=request.user)

    if request.method == 'POST':
        if u_form.is_valid() and p_form.is_valid():
            print("Selected course:", p_form.cleaned_data.get('course')) #Debugging
            u_form.save()

            student = p_form.save(user=request.user, commit=False)

            student.save()

            course = p_form.cleaned_data.get('course')
            if course:
                request.user.groups.clear()
                request.user.groups.add(course)
                print("User groups after update:", request.user.groups.all())
            else:
                request.user.groups.clear()

            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            print("u_form errors:", u_form.errors)
            print("p_form errors:", p_form.errors)
            messages.error(request, 'Error updating your profile. Please check the form.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentRegistrationForm(instance=request.user.student_profile)
        p_form.fields['course'].initial = request.user.groups.first()

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)



