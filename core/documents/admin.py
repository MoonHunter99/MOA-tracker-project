from django.contrib import admin
from .models import RequirementDocument

# Register your models here.

@admin.register(RequirementDocument)
class RequirementDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'specific_company')
    list_filter = ('specific_company',)
    search_fields = ('title', 'description')