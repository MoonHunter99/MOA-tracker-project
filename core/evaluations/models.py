from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.models import InternshipApplication


class InternshipEvaluation(models.Model):
    """
    A structured performance evaluation submitted by a company partner
    after a student completes their internship hours.
    Requires admin approval before becoming visible to the student.
    """
    REVIEW_STATUS_CHOICES = (
        ('pending_review', 'Pending Admin Review'),
        ('approved', 'Approved'),
    )

    RECOMMENDATION_CHOICES = (
        ('highly_recommended', 'Highly Recommended'),
        ('recommended', 'Recommended'),
        ('neutral', 'Neutral'),
        ('not_recommended', 'Not Recommended'),
    )

    # Core relationships
    application = models.OneToOneField(
        InternshipApplication,
        on_delete=models.CASCADE,
        related_name='evaluation'
    )
    evaluator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_evaluations'
    )

    # Admin approval gate
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default='pending_review'
    )

    # Structured rubric (1-5 scale)
    technical_skills = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the student's technical competence (1=Poor, 5=Excellent)"
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the student's communication skills (1=Poor, 5=Excellent)"
    )
    professionalism = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the student's professionalism (1=Poor, 5=Excellent)"
    )
    teamwork = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the student's teamwork ability (1=Poor, 5=Excellent)"
    )
    initiative = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the student's initiative and self-motivation (1=Poor, 5=Excellent)"
    )

    # Free-text and recommendation
    overall_comments = models.TextField(
        help_text="Provide overall feedback on the student's performance."
    )
    recommendation = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def average_score(self):
        """Returns the mean of all 5 rubric ratings."""
        scores = [
            self.technical_skills,
            self.communication,
            self.professionalism,
            self.teamwork,
            self.initiative,
        ]
        return round(sum(scores) / len(scores), 1)

    def __str__(self):
        student = self.application.student.username
        company = self.application.company.name
        return f"Evaluation: {student} at {company} ({self.get_review_status_display()})"
