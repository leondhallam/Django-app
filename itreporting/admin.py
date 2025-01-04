from django.contrib import admin
from .models import Issue
from .models import ContactSubmission
# from .models import Contact

# Register your models here.
admin.site.register(Issue)

# admin.site.register(Contact)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')  # Fields to display in the admin list view
    search_fields = ('name', 'email')  # Add a search bar for easy filtering
    list_filter = ('submitted_at',)  # Filter by submission date
