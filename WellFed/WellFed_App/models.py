from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Single_Meal_Manager(models.Manager):
    def create_meal(self, meal_name, meal_description, meal_type_choice, meal_date, recipe_link, calories, fats, carbs, sugar, sodium, protein, external_meal_id=None):
        meal = self.create(
            meal_name=meal_name,
            meal_description=meal_description,
            meal_type_choice=meal_type_choice,
            meal_date=meal_date,
            recipe_link=recipe_link,
            calories=calories,
            fats=fats,
            carbs=carbs,
            sugar=sugar,
            sodium=sodium,
            protien=protein,   # ✅ match field spelling
            meal_id=external_meal_id if external_meal_id else None,
        )
        return meal

class Single_Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Snack", "Snack"),
        ("Dessert", "Dessert"),
        ("Beverage", "Beverage"),
    ]

    meal_name = models.CharField(max_length=200)
    meal_description = models.TextField(blank=True)
    meal_type_choice = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default="Breakfast"
    )
    meal_id = models.IntegerField(blank=True, null=True)  # ✅ optional external ID
    meal_date = models.DateField(default=timezone.now)
    recipe_link = models.URLField(blank=True, null=True)
    calories = models.FloatField(default=0.0)
    fats = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    sugar = models.FloatField(default=0.0)
    sodium = models.FloatField(default=0.0)
    protien = models.FloatField(default=0.0)   # ✅ spelling consistent

    objects = Single_Meal_Manager()  # ✅ attach custom manager

    def __str__(self):
        return f"{self.meal_name} ({self.meal_type_choice})"

class Meal_Plan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Single_Meal, related_name="mealplans")
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user_id.username + " - " + str(self.date_created)

class Meal_Plan_Manager(models.Manager):
    def create_meal_plan(self, user_id, date_created=None):
        meal_plan = self.create(
            user_id=user_id,
            date_created=date_created if date_created else timezone.now()
        )
        return meal_plan

    def add_meal_to_plan(self, meal_plan, meal):
        meal_plan.meals.add(meal)
        return meal_plan