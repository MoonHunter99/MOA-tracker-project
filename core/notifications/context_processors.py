from notifications.models import Notification


def unread_notification_count(request):
    """
    Context processor that injects unread_count into every template
    so the navbar bell badge can display it globally.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}
