from django.contrib import admin
from .models import InternshipApplication

# Register your models here.

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'status', 'applied_on')
    list_filter = ('status',)