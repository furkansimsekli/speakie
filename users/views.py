from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from . import forms


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
                return redirect('course-list')  # TODO: redirect to landing page

        messages.warning(request,
                         'Given username or password does not belong to a user, please make sure they are correct!')
        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('course-list')  # TODO: redirect to landing page


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
