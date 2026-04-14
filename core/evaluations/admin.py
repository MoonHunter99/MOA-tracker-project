from django.contrib import admin
from .models import InternshipEvaluation


@admin.register(InternshipEvaluation)
class InternshipEvaluationAdmin(admin.ModelAdmin):
    list_display = ('application', 'evaluator', 'average_score', 'review_status', 'created_at')
    list_filter = ('review_status', 'recommendation')
    readonly_fields = ('created_at',)
