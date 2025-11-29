from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm
from .models import Single_Meal, Meal_Plan
from django.db.models import Q
import datetime
from django.utils import timezone
from django.contrib import messages
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import calendar
import random 



def meal_planner_view(request, view_type='day', offset=0):
    view_type = request.GET.get("view_type", "day")
    current_date_str = request.GET.get("date")
    current_date = None
    if current_date_str:
        try:
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d").date()
        except ValueError:
            try:
                current_date = datetime.strptime(current_date_str, "%b. %d, %Y").date()
            except ValueError:
                current_date = timezone.now().date()
    else:
        current_date = timezone.now().date()

    # Define start_date and end_date based on view_type
    if view_type == "day":
        start_date = current_date
        end_date = current_date
        prev_date = current_date - timedelta(days=1)
        next_date = current_date + timedelta(days=1)

    elif view_type == "week":
        start_date = current_date - timedelta(days=current_date.weekday())  # Monday
        end_date = start_date + timedelta(days=6)  # Sunday
        prev_date = start_date - timedelta(weeks=1)
        next_date = start_date + timedelta(weeks=1)

    elif view_type == "month":
        start_date = current_date.replace(day=1)
        # crude month end: add 30 days then back up to last day
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        prev_date = start_date - timedelta(days=30)
        next_date = start_date + timedelta(days=30)

    # Now you can safely query
    meal_plans = Meal_Plan.objects.filter(
        user_id=request.user,
        date_created__range=[start_date, end_date]
    )

    days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    meal_types = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Beverage"]

    grid = {day: {mt: [] for mt in meal_types} for day in days}

    for plan in meal_plans:
        plan_day = plan.date_created
        for meal in plan.meals.all():
            if meal.meal_type_choice in grid[plan_day]:
                grid[plan_day][meal.meal_type_choice].append(meal)

    # Pre-process rows
    grid_rows = []
    for meal_type in meal_types:
        row = {"meal_type": meal_type, "cells": []}
        for day in days:
            row["cells"].append(grid[day][meal_type])
        grid_rows.append(row)

    # Nutrition summary
    summary = {
        "calories": 0,
        "fats": 0,
        "carbs": 0,
        "sugar": 0,
        "sodium": 0,
        "protein": 0,
    }
    for plan in meal_plans:
        for meal in plan.meals.all():
            summary["calories"] += float(meal.calories or 0)
            summary["fats"] += float(meal.fats or 0)
            summary["carbs"] += float(meal.carbs or 0)
            summary["sugar"] += float(meal.sugar or 0)
            summary["sodium"] += float(meal.sodium or 0)
            summary["protein"] += float(meal.protien or 0)

    # Get preference from GET or POST
    preference = request.GET.get("preference", "")

    # Example: chatbot search function (replace with your actual API call)
    chatbot_results = []
    if preference:
        chatbot_results = run_chatbot_search(preference)[:3]
    else:
        chatbot_results = []



    # Random 3 meals from DB
    db_meals = list(Single_Meal.objects.all())
    random_meals = random.sample(db_meals, min(3, len(db_meals)))

    suggestions = {
        "preference": preference,
        "chatbot": chatbot_results,
        "random": random_meals,
    }

    target_calories = 2000
    total_calories = summary["calories"]
    total_fats = summary["fats"]
    total_carbs = summary["carbs"]
    total_protein = summary["protein"]
    total_sugar = summary["sugar"]
    target_sugar = 35
    target_protien = 150
    target_carbs = 250
    target_fats = 70 
    calorie_percent = (total_calories / target_calories) * 100 if target_calories else 0
    today_date = timezone.now().date()

    # scale targets depending on view_type
    if view_type == "week":
        multiplier = 7
    elif view_type == "month":
        # get number of days in the current month
        multiplier = calendar.monthrange(current_date.year, current_date.month)[1]
    else:
        multiplier = 1

    weekly_or_monthly_targets = {
        "target_calories": target_calories * multiplier,
        "target_protein": target_protien * multiplier,
        "target_carbs": target_carbs * multiplier,
        "target_fats": target_fats * multiplier,
    }

    return render(request, "mealPlanner.html", {
        "meal_plans": meal_plans,
        "grid_rows": grid_rows,
        "suggestions": suggestions,
        "view_type": view_type,
        "days": days,
        "current_date": current_date,
        "start_date": start_date,
        "end_date": end_date,
        "prev_date": prev_date,
        "next_date": next_date,
        "summary": summary,
        "offset": int(offset),
        "target_calories": target_calories,
        "calorie_percent": calorie_percent,
        "target_protein": target_protien,
        "target_carbs": target_carbs,
        "target_fats": target_fats,
        "target_sugar": target_sugar,
        "total_sugar": total_sugar,
        "total_calories": total_calories,
        "total_carbs": total_carbs,
        "total_fats": total_fats,
        "total_protein": total_protein,
        "today_date": today_date,
        **weekly_or_monthly_targets,
    })

# helpers.py or inside views.py
def run_chatbot_search(request_or_query):
    if hasattr(request_or_query, "GET"):
        query = request_or_query.GET.get("q", "")
    else:
        query = request_or_query  # assume it's a string

    # run chatbot API with query
    results = call_chatbot_api(query)
    return results

def call_chatbot_api(query: str):
    """
    Calls the FatSecret API to search for recipes matching the query.
    Returns a list of recipe dictionaries with nutrition info.
    """
    if not query:
        return []

    token = get_fatsecret_token()
    url = "https://platform.fatsecret.com/rest/server.api"
    params = {
        "method": "recipes.search",
        "search_expression": query,
        "format": "json",
        "max_results": 10
    }
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        recipes_data = data.get("recipes", {})
        recipe_list = recipes_data.get("recipe", [])

        results = []
        for recipe in recipe_list:
            results.append({
                "title": recipe.get("recipe_name"),
                "link": recipe.get("recipe_url", ""),
                "description": recipe.get("recipe_description", ""),
                "calories": recipe.get("recipe_nutrition", {}).get("calories", 0),
                "fats": recipe.get("recipe_nutrition", {}).get("fat", 0),
                "carbs": recipe.get("recipe_nutrition", {}).get("carbohydrate", 0),
                "sugar": recipe.get("recipe_nutrition", {}).get("sugar", 0),
                "sodium": recipe.get("recipe_nutrition", {}).get("sodium", 0),
                "protein": recipe.get("recipe_nutrition", {}).get("protein", 0),
            })
        return results

    except Exception as e:
        print("Error calling FatSecret API:", e)
        return []


def search_recipes(request):
    query = request.GET.get("q", "")
    results = Single_Meal.objects.filter(
        Q(meal_name__icontains=query) | Q(meal_description__icontains=query)
    )
    return render(request, "search.html", {"results": results, "query": query})

def chatbot_search(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        token = get_fatsecret_token()
        url = "https://platform.fatsecret.com/rest/server.api"
        params = {
            "method": "recipes.search",
            "search_expression": query,
            "format": "json",
            "max_results": 10
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        recipes_data = data.get("recipes", {})
        recipe_list = recipes_data.get("recipe", [])
        print("FatSecret response:", data)

    for recipe in recipe_list:
        results.append({
            "title": recipe.get("recipe_name"),
            "link": recipe.get("recipe_url", ""),
            "description": recipe.get("recipe_description", ""),
            "calories": recipe.get("recipe_nutrition", {}).get("calories", 0),
            "fats": recipe.get("recipe_nutrition", {}).get("fat", 0),
            "carbs": recipe.get("recipe_nutrition", {}).get("carbohydrate", 0),
            "sugar": recipe.get("recipe_nutrition", {}).get("sugar", 0),
            "sodium": recipe.get("recipe_nutrition", {}).get("sodium", 0),
            "protein": recipe.get("recipe_nutrition", {}).get("protien", 0),
        })
    
    return render(request, "chatbot_results.html", {"query": query, "results": results})

def add_recipe_to_mealplan(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        calories = float(request.POST.get("calories", 0))
        fats = float(request.POST.get("fats", 0))
        carbs = float(request.POST.get("carbs", 0))
        sugar = float(request.POST.get("sugar", 0))
        protein = float(request.POST.get("protein", 0))

        meal_type_choice = request.POST.get("meal_type_choice")
        meal_date_str = request.POST.get("meal_date")

        # Parse date correctly
        if meal_date_str:
            target_date = datetime.strptime(meal_date_str, "%Y-%m-%d").date()
        else:
            target_date = timezone.now().date()

        # Create Single_Meal
        meal = Single_Meal.objects.create(
            meal_name=title,
            meal_description=description,
            recipe_link=link,
            calories=calories,
            fats=fats,
            carbs=carbs,
            sugar=sugar,
            protien=protein,
            meal_type_choice=meal_type_choice,  # ✅ use user choice
            meal_date=target_date               # ✅ use user date
        )

        # Add to meal plan
        mealplan, created = Meal_Plan.objects.get_or_create(user_id=request.user, date_created=target_date)
        mealplan.meals.add(meal)

        messages.success(request, f"{title} was added to your {meal_type_choice} plan for {target_date}!")
        return redirect("meal_planner_view")

@csrf_exempt
def add_to_mealplan(request):
    if request.method == "POST":
        meal_id = request.POST.get("meal_id")
        meal_type_choice = request.POST.get("meal_type_choice")
        meal_date = request.POST.get("meal_date")

        recipe = get_object_or_404(Single_Meal, id=meal_id)

        # Use selected date, fallback to today
        target_date = datetime.datetime.strptime(meal_date, "%Y-%m-%d").date() if meal_date else timezone.now().date()

        mealplan, created = Meal_Plan.objects.get_or_create(user_id=request.user, date_created=target_date)

        # Update meal type if user selected one
        if meal_type_choice:
            recipe.meal_type_choice = meal_type_choice
            recipe.save()

        if mealplan.meals.filter(id=recipe.id).exists():
            messages.warning(request, f"{recipe.meal_name} is already in your {meal_type_choice} plan for {target_date}.")
        else:
            mealplan.meals.add(recipe)
            messages.success(request, f"{recipe.meal_name} was added to your {meal_type_choice} plan for {target_date}!")

        return JsonResponse({"success": True})

def get_fatsecret_token():
    client_id = "128cf53112494edbbbed50e9fc7f0009"
    client_secret = "9d07428a37f1448993c3a79324d26f14"
    url = "https://oauth.fatsecret.com/connect/token"
    data = {"grant_type": "client_credentials", "scope": "basic"}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()["access_token"]


def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("meal_planner_view", view_type="day")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("meal_planner_view", view_type="day")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, "logout.html")

