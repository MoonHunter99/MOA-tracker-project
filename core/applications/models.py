from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

# Create your models here.
class InternshipApplication(models.Model):
    APP_STATUS = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=10, choices=APP_STATUS, default='PENDING')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.company.name}"




class StudentProfile(models.Model):
    COURSE_CHOICES = [
        ('BSCpE', 'BS Computer Engineering'),
        ('BSIT', 'BS Information Technology'),
        ('BSCS', 'BS Computer Science'),
        ('BSEE', 'BS Electrical Engineering'),
        ('BSME', 'BS Mechanical Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.course}"