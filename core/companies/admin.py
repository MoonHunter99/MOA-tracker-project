from django.contrib import admin
from .models import Tag, Company

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'website', 'is_active')
    list_filter = ('is_active', 'tags')
    search_fields = ('name', 'description')