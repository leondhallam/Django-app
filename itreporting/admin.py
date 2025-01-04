from django.contrib import admin
from .models import Issue
from .models import ContactSubmission
# from .models import Contact

# Register your models here.
admin.site.register(Issue)

# admin.site.register(Contact)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('submitted_at',)
