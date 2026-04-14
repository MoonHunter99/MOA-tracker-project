from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from moas.models import MOA, MOARequest
from notifications.models import Notification


def send_moa_status_email(moa_request_id):
    """
    Background task: sends an email notification to the student
    when an admin updates their MOA request status.
    Called asynchronously via django-q2.
    """
    try:
        moa_request = MOARequest.objects.select_related('student').get(pk=moa_request_id)
    except MOARequest.DoesNotExist:
        return f"MOA Request {moa_request_id} not found."

    subject = f"Update: Your MOA Request for {moa_request.target_company_name}"
    message = (
        f"Hello {moa_request.student.username},\n\n"
        f"Your MOA Request for {moa_request.target_company_name} has been updated to: "
        f"{moa_request.get_status_display()}.\n\n"
        f"Thank you,\nPUP Admin Team"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [moa_request.student.email],
        fail_silently=True,
    )
    return f"Email sent to {moa_request.student.email} for MOA Request {moa_request_id}."


def check_moa_expiry():
    """
    Scheduled background task (runs daily via django-q2).
    Finds all active MOAs expiring within the next 30 days
    and creates notifications for all admin/staff users.
    """
    threshold_date = date.today() + timedelta(days=30)
    expiring_moas = MOA.objects.filter(
        is_active=True,
        expiration_date__lte=threshold_date,
        expiration_date__gte=date.today()
    ).select_related('company')

    if not expiring_moas.exists():
        return "No MOAs expiring within 30 days."

    admin_users = User.objects.filter(is_staff=True)
    created_count = 0

    for moa in expiring_moas:
        days_left = (moa.expiration_date - date.today()).days
        for admin_user in admin_users:
            # Avoid duplicate notifications for the same MOA on the same day
            already_notified = Notification.objects.filter(
                user=admin_user,
                title__contains=moa.company.name,
                created_at__date=date.today()
            ).exists()
            
            if not already_notified:
                Notification.objects.create(
                    user=admin_user,
                    title=f"MOA Expiring Soon: {moa.company.name}",
                    message=f"The MOA with {moa.company.name} expires on {moa.expiration_date.strftime('%B %d, %Y')} ({days_left} days remaining).",
                    link="/dashboard/admin/moas/"
                )
                created_count += 1

    return f"Created {created_count} expiry notifications for {expiring_moas.count()} MOAs."
