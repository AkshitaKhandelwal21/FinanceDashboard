from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import ExpenseForm, IncomeForm, BudgetForm
from .models import Budget

def index(request):
    return render(request, 'index.html')

# Sign-Up View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


# Add Expense View
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            print(f'Current logged-in user: {request.user}')  # Check who is the logged-in user
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')    
    else:
        form = ExpenseForm()
        print(f'Current logged-in user: {request.user}')
    return render(request, 'expense.html', {'form': form})


# Add Income View
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'income.html', {'form': form})


@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget added successfully!')
            return redirect('budget_dashboard')
    else:
        form = BudgetForm()
    return render(request, 'add_budget.html', {'form': form})


@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget_dashboard')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'edit_budget.html', {'form': form})


@login_required
def budget_dashboard(request):
    budgets = Budget.objects.filter(user=request.user, month=timezone.now().month, year=timezone.now().year)
    budget_data = []

    for budget in budgets:
        total_spent = budget.get_total_expenses()  # Get total expenses for the category
        remaining = budget.remaining_amount()  # Get remaining budget
        
        # Check if spending exceeds the threshold
        alert = False
        if budget.notification_threshold and total_spent > budget.notification_threshold / 100 * budget.amount:
            alert = True

        budget_data.append({
            'category': budget.category,
            'budgeted': budget.amount,
            'spent': total_spent,
            'remaining': remaining,
            'alert': alert,
        })

    return render(request, 'budget_overview.html', {'budget_data': budget_data})