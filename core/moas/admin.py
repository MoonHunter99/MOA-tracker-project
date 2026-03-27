from django.contrib import admin
from .models import MOA, MOARequest

# Register your models here.

@admin.register(MOA)
class MOAAdmin(admin.ModelAdmin):
    list_display = ('company', 'date_signed', 'expiration_date', 'is_active')
    list_filter = ('is_active', 'date_signed')
    search_fields = ('company__name',)

@admin.register(MOARequest)
class MOARequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'target_company_name', 'status', 'date_requested')
    list_filter = ('status', 'date_requested')
    search_fields = ('target_company_name', 'student__username')