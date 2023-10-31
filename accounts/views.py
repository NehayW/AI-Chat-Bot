from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import os


class UserSignup(View):
    """If the user is authenticated he is redirected to Home Page,
    else the user is directed to Sign-Up page"""
    def get(self, request):
        try:
            if request.user.is_authenticated:
                return redirect("chat:home")
            form = CreateUserForm()
            return render(request, "signup.html", {"form": form})
        except Exception as e:
            messages.error(request, str(e))
            return redirect("/")

    """If the sign-up is completed successfully user is directed to login page,
    else the errors are shown on sign-up page."""
    def post(self, request):
        try:
            form = CreateUserForm(request.POST)
            if not form.is_valid():
                return render(
                    request, "signup.html", {"form": form, "errors": form.errors}
                )
            form.save()
            return redirect("login")
        except Exception as e:
            messages.error(request, str(e))
            return redirect("/")


class UserLogin(View):

    def get(self, request):
        # Get Login Form
        if request.user.is_authenticated:
            return redirect("chat:home")
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    """If login is successful user is directed to home page,
    else error is displayed on login page"""
    def post(self, request):
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect("chat:home")
                else:
                    messages.warning(request, "Invalid Username or Password")
                    return redirect("login")
            else:
                return render(
                    request, "login.html", {"form": form, "errors": form.errors}
                )
        except Exception as e:
            messages.error(request, str(e))
            return redirect("sign-up")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("sign-up")
