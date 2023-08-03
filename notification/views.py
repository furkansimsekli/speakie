from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Notification


class NotificationReadStatusView(View):
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)

        if notification.owner == request.user:
            notification.is_read = True
            notification.save()
            return HttpResponse()

        return HttpResponseForbidden()
