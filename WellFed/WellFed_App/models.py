from django.db import models

# Create your models here.


class Single_Meal_Manager(models.Manager):
    def create_meal(self, meal_name, meal_id, user_id, recipe_link, meal_description, meal_type_choice, calories, protein, carbs, fats):
        meal = self.create(
            meal_name=meal_name,
            meal_id=meal_id,
            user_id=user_id,
            recipe_link=recipe_link,
            meal_description=meal_description,
            meal_type_choice=meal_type_choice,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
        return meal
#Defining attributes of a single meal
class Single_Meal (models.Model):
    meal_name = models.CharField(max_length=100)
    meal_id = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(max_length=50)
    recipe_link = models.URLField()
    meal_type_choice = models.CharField(max_length=50)
    meal_description = models.TextField()
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    objects = Single_Meal_Manager()

    def __str__(self):
        return self.meal_name
