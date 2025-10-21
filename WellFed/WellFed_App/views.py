from django.shortcuts import render
from . import models, forms
# Create your views here.
#Creating a view of the meal planner page 
def meal_planner_view(request):
    single_meals = models.Single_Meal.objects.all() #returns all single meals from the database
    return render(request, 'meal_planner.html', {'single_meals': single_meals})