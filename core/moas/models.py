from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

# Create your models here.

class MOA(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='moa')
    document_file = models.FileField(upload_to='moa_documents/')
    date_signed = models.DateField()
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"MOA - {self.company.name}"

class MOARequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('processing', 'Processing with Legal/Admin'),
        ('approved', 'Approved & Signed'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moa_requests')
    target_company_name = models.CharField(max_length=255)
    company_contact_person = models.CharField(max_length=255)
    company_contact_email = models.EmailField()
    justification = models.TextField(help_text="Why do you want to intern here?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MOA Request: {self.target_company_name} by {self.student.username}"