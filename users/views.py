from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from itreporting.models import Student
from .forms import UserRegistrationForm, StudentRegistrationForm
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        # Create user form and student registration form
        user_form = UserCreationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and student_form.is_valid():
            # Create the user object
            user = user_form.save()

            # Save the student profile and associate it with the user
            student = student_form.save(user=user, commit=False)  # Pass the user here
            student.save()

            # Notify the user of successful registration
            messages.success(request, 'Your account has been created successfully!')

            return redirect('login')  # Or redirect to some other page

        else:
            # Debugging: Print errors if forms are invalid
            print("user_form errors:", user_form.errors)
            print("student_form errors:", student_form.errors)
            messages.error(request, 'Error during registration. Please check the form.')

    else:
        user_form = UserCreationForm()
        student_form = StudentRegistrationForm()

    context = {
        'user_form': user_form,
        'student_form': student_form,
    }

    return render(request, 'users/register.html', context)


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



