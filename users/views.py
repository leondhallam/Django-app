from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, StudentRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentRegistrationForm(request.POST, request.FILES, instance=request.user.student_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            student = p_form.save(user=request.user, commit=False)
            student.user = request.user
            student.save()

            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            print("u_form errors:", u_form.errors)
            print("p_form errors:", p_form.errors)
            messages.error(request, 'Error updating your profile. Please check the form.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentRegistrationForm(instance=request.user.student_profile)

    student_modules = request.user.student_profile.modules.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'student_modules': student_modules,
    }

    return render(request, 'users/profile.html', context)





