from django.db import models
from companies.models import Company

# Create your models here.

class RequirementDocument(models.Model):
    title = models.CharField(max_length=255) # e.g., 'OJT Recommendation Letter Template'
    file = models.FileField(upload_to='application_requirements/')
    description = models.TextField(blank=True, null=True)
    
    # If a document is specific to one company, link it here. 
    # If left blank, it is treated as a general university requirement.
    specific_company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='specific_documents', 
        null=True, 
        blank=True
    )

    def __str__(self):
        if self.specific_company:
            return f"{self.title} ({self.specific_company.name})"
        return f"{self.title} (General PUP Requirement)"