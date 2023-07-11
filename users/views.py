from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms import UserRegisterForm, LoginForm, UserUpdateForm
from .models import Profile, Student, Moderator


class StudentRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            profile = Profile(user=user)  # TODO: use signals?
            profile.save()
            student = Student(profile=profile)
            student.save()

            messages.success(request, 'Yeyyy! You successfully joined to Speakie!')
            return redirect('login')

        return render(request, 'users/register.html', {'form': form})


class ModeratorRegisterView(View):
    def get(self, request):
        print("DEBUG: MOD REGISTER GET")  # TODO: Debug
        form = UserRegisterForm()
        return render(request, 'users/mod_register.html', {'form': form})

    def post(self, request):
        print("DEBUG: MOD REGISTER POST 1")  # TODO: Debug
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            print("DEBUG: MOD REGISTER POST 2")  # TODO: Debug
            user = form.save()

            profile = Profile(user=user)  # TODO: use signals?
            profile.save()
            moderator = Moderator(profile=profile)
            moderator.save()
            print("DEBUG: MOD REGISTER POST 3")  # TODO: Debug

            messages.success(request, 'Yeyyy! You successfully joined to Speakie!')
            return redirect('login')

        return render(request, 'users/mod_register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)

        context = {
            'u_form': u_form,
        }

        return render(request, 'users/profile.html', context)

    def post(self, request):
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)

            if u_form.is_valid():
                u_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)

        context = {
            'u_form': u_form,
        }

        return render(request, 'users/profile.html', context)
