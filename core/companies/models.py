from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    COURSE_CHOICES = [
        ('BSCpE', 'BS Computer Engineering'),
        ('BSIT', 'BS Information Technology'),
        ('BSCS', 'BS Computer Science'),
        ('BSEE', 'BS Electrical Engineering'),
        ('BSME', 'BS Mechanical Engineering'),
        # Add more PUP courses as needed
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active MOA'),
        ('EXPIRED', 'Expired'),
        ('PENDING', 'Under Review'),
        ('NONE', 'No MOA'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    
    # Classification for courses
    course_tag = models.CharField(max_length=10, choices=COURSE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NONE')
    
    # MOA Details
    moa_file = models.FileField(upload_to='moas/', null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.course_tag})"

class MOARequest(models.Model):
    """Model for students to suggest a company not on the list"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    contact_person = models.CharField(max_length=100)
    request_date = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for {self.company_name} by {self.student.username}"

