from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def is_over_budget(self):
        return self.total_spent > self.total_budget

    def __str__(self):
        return f"{self.user.username}'s Budget"
