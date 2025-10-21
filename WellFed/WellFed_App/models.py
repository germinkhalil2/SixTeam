from django.db import models

# Create your models here.
class Single_Meal (models.Model):
    meal_name = models.CharField(max_length=100)
    meal_id = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(max_length=50)
    recipe_link = models.URLField()
    meal_type_choice = [ ('Breakfast', 'breakfast'), ('Lunch', 'lunch'), ('Dinner', 'dinner'), ('Snack', 'snack'), ('Dessert', 'dessert'), ('Drink', 'drink') ]
    meal_description = models.TextField()
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
        return self.meal_name