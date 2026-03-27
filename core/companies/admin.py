from django.contrib import admin
from .models import Company, MOARequest

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # This controls what columns show up in the list view
    list_display = ('name', 'course_tag', 'status', 'expiry_date')
    # Adds a sidebar filter
    list_filter = ('status', 'course_tag')
    # Adds a search bar
    search_fields = ('name', 'contact_person')

@admin.register(MOARequest)
class MOARequestAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'student', 'request_date', 'is_processed')
    list_filter = ('is_processed',)