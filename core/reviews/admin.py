from django.contrib import admin
from .models import CompanyReview

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'overall_rating', 'status', 'created_at')
    list_filter = ('status', 'overall_rating')
    search_fields = ('student__username', 'company__name', 'pros', 'cons')
