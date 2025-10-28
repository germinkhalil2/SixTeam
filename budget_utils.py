# budget_utils.py
from typing import Iterable

def calculate_total_expenses(expenses: Iterable[float]) -> float:
    """Return the sum of the expenses (floats or ints)."""
    return sum(float(e) for e in expenses)

def calculate_remaining(budget: float, expenses: Iterable[float]) -> float:
    """
    Return remaining budget after subtracting expenses.
    If budget is negative or invalid, raises ValueError.
    """
    try:
        budget = float(budget)
    except (TypeError, ValueError):
        raise ValueError("budget must be a number")

    total = calculate_total_expenses(expenses)
    return budget - total

def can_add_expense(budget: float, expenses: Iterable[float], new_expense: float) -> bool:
    """
    Return True if new_expense can be added without exceeding budget.
    """
    try:
        new_expense = float(new_expense)
    except (TypeError, ValueError):
        raise ValueError("new_expense must be a number")

    remaining = calculate_remaining(budget, expenses)
    return (remaining - new_expense) >= 0
