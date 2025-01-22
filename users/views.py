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
        user_form = UserCreationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()

            student = student_form.save(user=user, commit=False)
            student.save()

            messages.success(request, 'Your account has been created successfully!')

            return redirect('login')

        else:
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
    user = request.user
    student_profile = user.student_profile

    registered_modules = student_profile.modules.all()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentRegistrationForm(request.POST, request.FILES, instance=request.user.student_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            student = p_form.save(commit=False)
            student.user = request.user
            student.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentRegistrationForm(instance=request.user.student_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'registered_modules': registered_modules,
    }

    return render(request, 'users/profile.html', context)

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    user_courses = request.user.groups.all()

    if request.method == 'POST':
        if any(course in user_courses for course in module.courses_allowed.all()):
            if 'register' in request.POST:
                ModuleRegistration.objects.create(user=request.user, module=module)
                messages.success(request, f'You have successfully registered for {module.name}')
            elif 'unregister' in request.POST:
                registration = ModuleRegistration.objects.filter(user=request.user, module=module).first()
                if registration:
                    registration.delete()
                    messages.success(request, f'You have successfully unregistered from {module.name}')
        else:
            messages.error(request, 'You must be enrolled in a course that allows this module to register.')

        return redirect('module_detail', module_id=module.id)

    context = {'module': module}
    return render(request, 'itreporting/module_detail.html', context)

