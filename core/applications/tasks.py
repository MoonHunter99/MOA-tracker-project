from django.core.mail import send_mail
from django.conf import settings
from applications.models import InternshipApplication


def send_status_email(application_id):
    """
    Background task: sends an email notification to the student
    when an admin updates their application status.
    Called asynchronously via django-q2.
    """
    try:
        application = InternshipApplication.objects.select_related('student', 'company').get(pk=application_id)
    except InternshipApplication.DoesNotExist:
        return f"Application {application_id} not found."

    subject = f"Update: Your Internship Application for {application.company.name}"
    message = (
        f"Hello {application.student.username},\n\n"
        f"Your application status for {application.company.name} has been updated to: "
        f"{application.get_status_display()}.\n\n"
        f"Thank you,\nPUP Admin Team"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [application.student.email],
        fail_silently=True,
    )
    return f"Email sent to {application.student.email} for application {application_id}."
