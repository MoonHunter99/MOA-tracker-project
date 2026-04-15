from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from companies.models import Company
from applications.models import InternshipApplication


# Words that will trigger automatic flagging for admin review
BLOCKLIST = [
    'scam', 'fraud', 'illegal', 'harassment', 'abuse', 'racist',
    'sexist', 'discriminat', 'exploit', 'threat', 'bribe', 'corrupt',
    'hate', 'assault', 'obscen', 'profan',
]


def contains_blocked_content(text):
    """Check if text contains any blocklisted word (case-insensitive, substring match)."""
    text_lower = text.lower()
    return any(word in text_lower for word in BLOCKLIST)


class CompanyReview(models.Model):
    """
    Structured feedback from a student about their internship experience
    at a specific company. Auto-moderated via keyword blocklist.
    """
    REVIEW_STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('pending_review', 'Pending Admin Review'),
    )

    # Core relationships
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_reviews')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    application = models.OneToOneField(
        InternshipApplication,
        on_delete=models.CASCADE,
        related_name='review',
        help_text="Ensures one review per completed internship"
    )

    # Structured ratings (1-5)
    overall_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Overall experience (1=Poor, 5=Excellent)"
    )
    mentorship_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Quality of mentorship (1=Poor, 5=Excellent)"
    )
    work_culture_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Work environment and culture (1=Poor, 5=Excellent)"
    )
    learning_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Learning opportunities (1=Poor, 5=Excellent)"
    )

    # Written feedback
    pros = models.TextField(help_text="What did you enjoy about the internship?")
    cons = models.TextField(help_text="What could be improved?")
    advice = models.TextField(blank=True, default='', help_text="Any advice for future interns?")

    # Privacy and moderation
    is_anonymous = models.BooleanField(default=False, help_text="Hide your name on the public review")
    status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='approved')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'application')
        ordering = ['-created_at']

    @property
    def average_rating(self):
        """Returns the mean of all 4 category ratings."""
        scores = [
            self.overall_rating,
            self.mentorship_rating,
            self.work_culture_rating,
            self.learning_rating,
        ]
        return round(sum(scores) / len(scores), 1)

    def __str__(self):
        student_name = "Anonymous" if self.is_anonymous else self.student.username
        return f"Review: {student_name} on {self.company.name} ({self.get_status_display()})"
