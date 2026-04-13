from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

# Create your models here.

class InternshipApplication(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted to Company'),
        ('interviewing', 'Interviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    application_date = models.DateTimeField(auto_now_add=True)
    student_resume = models.FileField(upload_to='student_resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.username} -> {self.company.name} ({self.get_status_display()})"

class ApplicationMessage(models.Model):
    application = models.ForeignKey(InternshipApplication, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # helper to easily style the UI (left/right alignment)
    is_from_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Msg by {self.sender.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"