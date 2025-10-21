from django.test import TestCase
from .models import Single_Meal

# Create your tests here.
class SingleMealTestCase(TestCase):
    def setUp(self):
        # Set up a test meal
        Single_Meal.objects.create_meal(
            meal_name="Pancakes",
            meal_id="121",
            user_id="121",
            recipe_link="http://example.com/test-meal",
            meal_description="A test meal for unit testing.",
            meal_type_choice="Snack",
            calories=600,
            protein=40.0,
            carbs=50.0,
            fats=20.0
        )

    def test_meal_creation(self):
        # Test if the meal was created successfully
        meal = Single_Meal.objects.get(meal_id="121")
        self.assertEqual(meal.meal_name, "Pancakes")
        self.assertEqual(meal.meal_type_choice, "Snack")
        self.assertEqual(meal.calories, 600)
        self.assertEqual(meal.protein, 40.0)
        self.assertEqual(meal.carbs, 50.0)
        self.assertEqual(meal.fats, 20.0)