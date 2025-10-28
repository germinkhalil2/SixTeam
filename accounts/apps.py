from django.shortcuts import render
from . import models, forms
from .models import Single_Meal

# Create your views here.

# Creating a view of the meal planner page
def meal_planner_view(request):
    # Testing meal creation below
    # Single_Meal.objects.create_meal("Test Meal", "1", "1", "http://example.com/recipe", "A delicious test meal.")
    # Single_Meal.objects.create_meal("Grilled Chicken Salad", "2", "1", "http://example.com/grilled-chicken-salad", "Healthy and tasty!")

    single_meals = Single_Meal.objects.all()  # returns all single meals from the database
    context = {'single_meals': single_meals}
    return render(request, 'mealPlanner.html', context)


def home_view(request):
    return render(request, 'home.html')