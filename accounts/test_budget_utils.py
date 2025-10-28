# test_budget_utils.py
from django.test import SimpleTestCase
from budget_utils import calculate_total_expenses, calculate_remaining, can_add_expense

class BudgetUtilsTests(SimpleTestCase):
    def test_calculate_total_expenses(self):
        expenses = [50, 30, 20]
        self.assertEqual(calculate_total_expenses(expenses), 100.0)

    def test_calculate_remaining_normal(self):
        budget = 150
        expenses = [50, 30, 20]
        self.assertEqual(calculate_remaining(budget, expenses), 50.0)

    def test_calculate_remaining_zero_budget(self):
        budget = 0
        expenses = []
        self.assertEqual(calculate_remaining(budget, expenses), 0.0)

    def test_can_add_expense_within_budget(self):
        budget = 150
        expenses = [50, 30, 20]
        self.assertTrue(can_add_expense(budget, expenses, 50))  # remaining 50, new 50 OK

    def test_cannot_add_expense_exceeding_budget(self):
        budget = 150
        expenses = [50, 30, 20]
        self.assertFalse(can_add_expense(budget, expenses, 60))  # remaining 50, new 60 fails

    def test_invalid_budget_raises(self):
        with self.assertRaises(ValueError):
            calculate_remaining("not-a-number", [10])

    def test_invalid_new_expense_raises(self):
        with self.assertRaises(ValueError):
            can_add_expense(100, [10], "bad")