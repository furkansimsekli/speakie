from django.urls import path
from . import views

urlpatterns = [
    path('<notification_id>/read/', views.NotificationReadStatusView.as_view(), name='notification-read')
]
