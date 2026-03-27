from django.db import models

# Create your models here.
class Tag(models.Model):
    # Examples: 'Software', 'Hardware', 'Embedded Systems', 'Flutter', 'DSP'
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='companies')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name