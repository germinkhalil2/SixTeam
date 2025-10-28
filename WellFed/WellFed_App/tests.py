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

class NutritionFactsTestCase(TestCase):
    def test_nutrition_facts_calculation(self):
        # Test the nutrition facts calculation logic
        meal = Single_Meal.objects.create_meal(
            meal_name="Salad",
            meal_id="122",
            user_id="122",
            recipe_link="http://example.com/salad-meal",
            meal_description="A healthy salad meal.",
            meal_type_choice="Lunch",
            calories=300,
            protein=10.0,
            carbs=20.0,
            fats=15.0
        )
        self.assertEqual(meal.calories, 300)
        self.assertEqual(meal.protein, 10.0)
        self.assertEqual(meal.carbs, 20.0)
        self.assertEqual(meal.fats, 15.0)