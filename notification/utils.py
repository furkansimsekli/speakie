from .models import Notification


def get_notifications(request):
    if request.user.is_authenticated:
        return {'notifications': Notification.objects.filter(owner=request.user, is_read=False).order_by('-id')}

    return {}
