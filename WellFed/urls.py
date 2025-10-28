# WellFed/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add the accounts app urls under /accounts/
    path("accounts/", include("accounts.urls")),
    # optional: redirect root to dashboard (change as needed)
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),
]
