from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View

from . import forms
from .models import User


class RegisterView(View):
    def get(self, request):
        form = forms.UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = forms.UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Yeyyy! You successfully joined to Speakie!')
            return redirect('login')

        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = forms.UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = forms.UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')

        messages.warning(request,
                         'Given username or password does not belong to a user, please make sure they are correct!')
        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileView(View):
    def get(self, request):
        form = forms.UserUpdateForm(instance=request.user)
        return render(request, 'users/profile.html', {'form': form})

    def post(self, request):
        form = forms.UserUpdateForm(request.POST,
                                    files=request.FILES,
                                    instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

        return render(request, 'users/profile.html', {'form': form})


class AppointModeratorView(View):
    def get(self, request):
        students = get_list_or_404(User, is_moderator=False)
        page = request.GET.get('page', 1)
        paginator = Paginator(students, per_page=10)
        page_object = paginator.get_page(page)
        return render(request, 'users/appoint_moderator.html', {'page_obj': page_object})

    def post(self, request):
        new_mod_id = request.POST.get('new_mod_id')
        user = get_object_or_404(User, id=new_mod_id)
        user.is_moderator = True
        user.save()
        messages.success(request, f'{user.username} has been appointed as moderator!')
        return redirect('appoint-moderator')
