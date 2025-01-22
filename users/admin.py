from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from itreporting.models import Student

admin.site.register(Profile)

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = "Student Profile"
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline,)

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_course')
    list_select_related = ('student',)

    def get_course(self, instance):
        """Display the user's course (Group) in the admin list view."""
        group = instance.groups.first()
        return group.name if group else "No course assigned"
    get_course.short_description = 'Course'

    def save_model(self, request, obj, form, change):
        """Ensure a Student profile is created automatically for a new User."""
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'student'):
            Student.objects.create(user=obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)