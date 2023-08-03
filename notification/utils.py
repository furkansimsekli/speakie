from .models import Notification


def get_notifications(request):
    return {'notifications': Notification.objects.filter(is_read=False).order_by('-id')}
