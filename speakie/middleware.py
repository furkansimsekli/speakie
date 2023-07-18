from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve

from .constants import MODERATOR_AUTHORIZED_URL_NAMES


class ModeratorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolved = resolve(request.path)

        if resolved.view_name in MODERATOR_AUTHORIZED_URL_NAMES and not request.user.is_moderator:
            messages.warning(request, 'You are not authorized to do this!')
            return redirect('course-list')

        response = self.get_response(request)
        return response
