# WellFed/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from accounts.views import home_view
from django.contrib.auth import views as auth_views
from accounts.views import budget_view

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add the accounts app urls under /accounts/
    path("accounts/", include("accounts.urls")),
    # optional: redirect root to dashboard (change as needed)
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("home/", home_view, name="home"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("budget/", budget_view, name="budget")
]