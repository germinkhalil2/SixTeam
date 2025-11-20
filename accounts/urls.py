# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views
from .views import signup_view
from .views import home_view
from .views import login_view

urlpatterns = [
    path("/accounts/signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("", login_view, name="login"),
    path("home/", home_view, name="home"),

]



