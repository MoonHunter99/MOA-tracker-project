from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from companies.models import Company

class StudentProfile(models.Model):
    COURSE_CHOICES = [
        ('BSCE', 'BS Civil Engineering'),
        ('BSCPE', 'BS Computer Engineering'),
        ('BSEE', 'BS Electrical Engineering'),
        ('BSIE', 'BS Industrial Engineering'),
        ('BSME', 'BS Mechanical Engineering'),
        ('BSRE', 'BS Railway Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True, blank=True)
    year_level = models.IntegerField(null=True, blank=True, choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year'), (5, '5th Year')])

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companyprofile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='representatives')

    def __str__(self):
        return f"{self.user.username} ({self.company.name})"

# Signal to automatically create a profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not getattr(instance, '_is_company_user', False):
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
