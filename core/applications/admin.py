from django.contrib import admin
from .models import InternshipApplication

# Register your models here.

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'status', 'application_date')
    list_filter = ('status', 'application_date')
    search_fields = ('student__username', 'company__name')