from allauth.socialaccount.views import SignupView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from . import forms, utils
from .models import User


class RegisterView(View):
    def get(self, request):
        form = forms.UserRegisterForm()
        return render(request, 'users/register.html', {'form': form, 'title': 'Join!'})

    def post(self, request):
        form = forms.UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=email, password=password)
            login(request, user)
            messages.success(request, 'Yeyyy! You successfully joined to Speakie!')
            return redirect('home')

        return render(request, 'users/register.html', {'form': form, 'title': 'Join!'})


class LoginView(View):
    def get(self, request):
        form = forms.UserLoginForm()
        return render(request, 'users/login.html', {'form': form, 'title': 'Login'})

    def post(self, request):
        form = forms.UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')

        messages.warning(request,
                         'Given username or password does not belong to a user, please make sure they are correct!')
        return render(request, 'users/login.html', {'form': form, 'title': 'Login'})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.UserUpdateForm(instance=request.user)
        level = utils.calculate_level(request.user.score)
        return render(request, 'users/profile.html', {'form': form, 'level': level, 'title': 'Profile'})

    def post(self, request):
        form = forms.UserUpdateForm(request.POST,
                                    files=request.FILES,
                                    instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

        return render(request, 'users/profile.html', {'form': form, 'title': 'Profile'})


class PasswordRequestView(View):
    def get(self, request):
        form = forms.PasswordResetRequestForm()
        return render(request, 'users/password_reset_request.html', context={'form': form, 'title': 'Password Reset'})

    def post(self, request):
        form = forms.PasswordResetRequestForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://localhost:8000/password-reset-confirm/{uid}/{token}/"
            subject = 'Speakie - Password Reset'
            message = (f'You requested a password reset, if this is not you, you can ignore this mail\n\n'
                       f'{reset_url}')
            send_mail(subject, message, '', [email])  # Sender's address is specified in settings.py
            messages.success(request, 'An email has been sent your address!')
            return redirect('password-reset-request')
        else:
            return render(request, 'users/password_reset_request.html',
                          context={'form': form, 'title': 'Password Reset'})


class PasswordResetView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = forms.PasswordResetForm()
            return render(request, 'users/password_reset_confirm.html',
                          {'form': form, 'uidb64': uidb64, 'token': token, 'title': 'Password Reset'})
        else:
            messages.warning(request, 'Invalid Request!')
            return redirect('home')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        form = forms.PasswordResetForm(request.POST)

        if form.is_valid():
            if user is not None and default_token_generator.check_token(user, token):
                new_password = request.POST.get('new_password')
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Voila, your password has been reset!')
                return redirect('login')
            else:
                messages.warning(request, 'Invalid Request!')
                return redirect('home')
        else:
            return render(request, 'users/password_reset_confirm.html',
                          {'form': form, 'uidb64': uidb64, 'token': token, 'title': 'Password Reset'})


class AppointModeratorView(LoginRequiredMixin, View):
    def get(self, request):
        students = User.objects.filter(is_moderator=False)
        page = request.GET.get('page', 1)
        paginator = Paginator(students, per_page=10)
        page_object = paginator.get_page(page)
        return render(request, 'users/appoint_moderator.html', {'page_obj': page_object, 'title': 'Appoint Moderator'})

    def post(self, request):
        new_mod_id = request.POST.get('new_mod_id')
        user = User.objects.filter(id=new_mod_id)
        user.is_moderator = True
        user.save()
        messages.success(request, f'{user.username} has been appointed as moderator!')
        return redirect('appoint-moderator')


class CustomSignupView(SignupView):
    http_method_names = ['get']

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email: str = self.sociallogin.user.email
        messages.warning(self.request, f'The account with {email} address is not connected to Google!')
        return redirect('login')
