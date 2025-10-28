from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Budget
from .forms import BudgetForm
from django.contrib.auth.decorators import login_required
@login_required
def budget_view(request):
    budget, created = Budget.objects.get_or_create(user=request.user)
    form = BudgetForm(request.POST or None, instance=budget)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully!")
    # Example spending logic (replace with your real spending tracker)
    total_spent = budget.total_spent  # You can update this from another model
    over_budget = budget.is_over_budget()
    if over_budget:
        messages.warning(request, f"⚠️ You have gone over your budget by ${total_spent - budget.total_budget}!")
    return render(request, 'budget.html', {'form': form, 'budget': budget, 'over_budget': over_budget})
