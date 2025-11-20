from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Budget
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()      # create the user
            login(request, user)    # log them in automatically
            return redirect("home") # redirect to homepage of meal planner
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})

@login_required
def home_view(request):
    return render(request, "home.html")
def dashboard_view(request):
    try:
        budget = Budget.objects.get(user=request.user)
    except Budget.DoesNotExist:
        budget = None
    return render(request, "accounts/dashboard.html", {"budget": budget})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home")  # Change 'home' to your app's main page name
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")