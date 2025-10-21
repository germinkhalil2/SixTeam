from django.test import TestCase
from .models import Single_Meal
from .models import user_preference
# Create your tests here.
class UserPreferenceTestCase(TestCase):
 def setUpPreferences(self):
        # Set up a test user preference
        user_preference.objects.create_preference(
            user_id="test_user",
            dietary_restrictions="None",
            cuisine_preferences="Italian, Mexican",
            calorie_goal=2000,
            protein_goal=150.0,
            carb_goal=250.0,
            fat_goal=70.0
        )
def test_preference_creation(self):
        # Test if the user preference was created successfully
        preference = user_preference.objects.get(user_id="test_user")
        self.assertEqual(preference.dietary_restrictions, "None")
        self.assertEqual(preference.cuisine_preferences, "Italian, Mexican")
        self.assertEqual(preference.calorie_goal, 2000)
        self.assertEqual(preference.protein_goal, 150.0)
        self.assertEqual(preference.carb_goal, 250.0)
        self.assertEqual(preference.fat_goal, 70.0)



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