"""
URL configuration for speakie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from base import views as base_views
from user import views as user_views

urlpatterns = [
    path('', base_views.HomeView.as_view(), name='home'),
    path('about/', base_views.AboutView.as_view(), name='about'),
    path('course/', include('course.urls')),
    path('notifications/', include('notification.urls')),
    path('admin/', admin.site.urls),
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('password-reset/', user_views.PasswordRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', user_views.PasswordResetView.as_view(), name='password-reset-confirm'),
    path('appoint-moderator/', user_views.AppointModeratorView.as_view(), name='appoint-moderator'),
    path('accounts/social/signup/', user_views.CustomSignupView.as_view(), name='social-signup'),
    path('accounts/', include('allauth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
