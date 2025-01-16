from django.contrib import admin
from .models import Issue
from .models import ContactSubmission
from .models import Student

# Register your models here.
admin.site.register(Issue)

# admin.site.register(Contact)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('submitted_at',)

from .models import Module, Student, Registration

# Module model
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'category', 'availability')
    list_filter = ('category', 'availability')
    search_fields = ('name', 'code')

# Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_course', 'date_of_birth', 'address', 'city_town', 'country')
    search_fields = ('user__username', 'user__email', 'address', 'city_town', 'country')

    def get_course(self, obj):
        groups = obj.user.groups.all()
        return groups.first().name if groups else "Not assigned"
    get_course.short_description = "Course"

admin.site.register(Student, StudentAdmin)

# Registration model
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'date_of_registration')
    search_fields = ('student__user__username', 'module__name', 'module__code')
    list_filter = ('date_of_registration',)