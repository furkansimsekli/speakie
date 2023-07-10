from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm


class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        print(request.POST)
        return render(request, 'users/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        print(request.POST.get('username'))
        return render(request, 'users/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
