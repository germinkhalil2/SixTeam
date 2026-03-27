from django import forms
#Create all user input forms here

#User input form for creating a single meal 
class SingleMealForm(forms.Form):
    meal_name = forms.CharField(max_length=100)
    meal_id = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50)
    recipe_link = forms.URLField()
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'breakfast'),
        ('Lunch', 'lunch'),
        ('Dinner', 'dinner'),
        ('Snack', 'snack'),
        ('Dessert', 'dessert'),
        ('Drink', 'drink'),
    ]
    meal_type = forms.ChoiceField(choices=MEAL_TYPE_CHOICES)
    meal_description = forms.CharField(widget=forms.Textarea)
    calories = forms.IntegerField()
    protein = forms.FloatField()
    carbs = forms.FloatField()
    fats = forms.FloatField()