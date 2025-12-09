# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        return redirect("login")

    return render(request, "accounts/signup.html")

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            # Role redirect
            if user.role == "doctor":
                return redirect("doctor_dashboard")
            else:
                return redirect("patient_dashboard")

        return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")



def logout_view(request):
    logout(request)
    return redirect("login")

