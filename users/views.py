from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, StudentRegistrationForm
from django.contrib.auth.decorators import login_required
from itreporting.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from itreporting.models import Module, ModuleRegistration

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
    # Get the user profile
    user = request.user
    student_profile = user.student_profile  # Assuming student profile is related to the User model

    # Fetch the modules that the student is registered for
    registered_modules = student_profile.modules.all()

    if request.method == 'POST':
        # Handle form submissions if needed (user and student profile update)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentRegistrationForm(request.POST, request.FILES, instance=request.user.student_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            student = p_form.save(commit=False)
            student.user = request.user
            student.save()
            # Handle course selection logic here (if needed)
            return redirect('profile')
    else:
        # Initialize the forms
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentRegistrationForm(instance=request.user.student_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'registered_modules': registered_modules,  # Pass the registered modules to the template
    }

    return render(request, 'users/profile.html', context)

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    user_courses = request.user.groups.all()

    if request.method == 'POST':
        # Check if the student is part of a course allowed to register for the module
        if any(course in user_courses for course in module.courses_allowed.all()):
            if 'register' in request.POST:
                # Register the student for the module
                ModuleRegistration.objects.create(user=request.user, module=module)
                messages.success(request, f'You have successfully registered for {module.name}')
            elif 'unregister' in request.POST:
                # Unregister the student
                registration = ModuleRegistration.objects.filter(user=request.user, module=module).first()
                if registration:
                    registration.delete()
                    messages.success(request, f'You have successfully unregistered from {module.name}')
        else:
            messages.error(request, 'You must be enrolled in a course that allows this module to register.')

        return redirect('module_detail', module_id=module.id)

    context = {'module': module}
    return render(request, 'itreporting/module_detail.html', context)

