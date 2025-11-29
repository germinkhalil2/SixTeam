"""
URL configuration for WellFed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, re_path
from WellFed_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meal_planner/', views.meal_planner_view, name="meal_planner_view"),  # ✅ added name
    path('home/', views.home_view, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("mealplan/<str:view_type>/", views.meal_planner_view, name="meal_plan"),
    path("search/", views.search_recipes, name="search_recipes"),
    path("add/", views.add_to_mealplan, name="add_to_mealplan"),
    path("mealplan/<str:view_type>/<int:offset>/", views.meal_planner_view, name="meal_plan_offset"),
    path("chatbot_search/", views.chatbot_search, name="chatbot_search"),
    path("add_recipe/", views.add_recipe_to_mealplan, name="add_recipe_to_mealplan"),
    path("", lambda request: render(request, "home.html"), name="home"),
    path("mealplanner/<str:view_type>/", views.meal_planner_view, name="meal_planner_view"),
    path("add-to-mealplan/", views.add_to_mealplan, name="add-to-mealplan"),
    re_path(r"^mealplan/(?P<view_type>[^/]+)/(?P<offset>-?\d+)/$", views.meal_planner_view, name="meal_plan_offset"),
]
