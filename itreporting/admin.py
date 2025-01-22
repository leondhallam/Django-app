from django.contrib import admin
from .models import Issue, ContactSubmission, Student, Module, Registration

# Register your models here.
admin.site.register(Issue)

# admin.site.register(Contact)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('submitted_at',)

# Module model
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'category', 'availability')
    list_filter = ('category', 'availability')
    search_fields = ('name', 'code')

# Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'list_modules')
    list_filter = ('course',)
    search_fields = ('user__username', 'user__email', 'course__name')
    autocomplete_fields = ['course']

    def list_modules(self, obj):
        return ", ".join([module.name for module in obj.modules.all()])
    list_modules.short_description = "Registered Modules"

    def save_model(self, request, obj, form, change):
        """
        Ensure the course is correctly set during the save operation.
        """
        if obj.course:
            print(f"Saving Student: {obj.user.username}, Course: {obj.course.name}")
        else:
            print(f"Saving Student: {obj.user.username}, No course assigned")
        super().save_model(request, obj, form, change)

    def course(self, obj):
        return obj.course.name if obj.course else "Not assigned"

# Registration model
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'date_of_registration')
    search_fields = ('student__user__username', 'module__name', 'module__code')
    list_filter = ('date_of_registration',)