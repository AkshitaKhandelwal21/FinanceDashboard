from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import ExpenseForm, IncomeForm, BudgetForm
from .models import Budget, Income, Expense
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from datetime import datetime


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
    income_data = Income.objects.values('date').annotate(total_income=Sum('amount'))
    expense_data = Expense.objects.values('date').annotate(total_expense=Sum('amount'))

    income_dates = [entry['date'] for entry in income_data]
    income_values = [entry['total_income'] for entry in income_data]

    expense_dates = [entry['date'] for entry in expense_data]
    expense_values = [entry['total_expense'] for entry in expense_data]

    # Create Plotly line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=income_dates, y=income_values, mode='lines+markers', name='Income'))
    fig.add_trace(go.Scatter(x=expense_dates, y=expense_values, mode='lines+markers', name='Expenses'))

    fig.update_layout(title='Income and Expenses Over Time', xaxis_title='Date', yaxis_title='Amount')
    chart1 = plot(fig, output_type='div')

    current_month = datetime.now().month
    current_year = datetime.now().year

    budgets = Budget.objects.filter(month=current_month, year=current_year).values('category').annotate(total_budget=Sum('amount'))
    expenses = Expense.objects.filter(date__month=current_month, date__year=current_year).values('category').annotate(total_expense=Sum('amount'))

    categories = [entry['category'] for entry in budgets]
    budget_values = [entry['total_budget'] for entry in budgets]
    expense_values = [entry['total_expense'] for entry in expenses if entry['category'] in categories]

    # Create Plotly bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=budget_values, name='Budgeted'))
    fig.add_trace(go.Bar(x=categories, y=expense_values, name='Actual'))

    fig.update_layout(barmode='group', title='Budget vs. Actual Expenses', xaxis_title='Category', yaxis_title='Amount')
    chart2 = plot(fig, output_type='div')


    expense_data = Expense.objects.values('category').annotate(total_amount=Sum('amount'))

    categories = [entry['category'] for entry in expense_data]
    amounts = [entry['total_amount'] for entry in expense_data]

    # Create Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=categories, values=amounts)])
    fig.update_layout(title='Spending by Category')
    chart3 = plot(fig, output_type='div')

    charts = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3
    }
    return render(request, 'dashboard.html', charts)


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
            print(f'Current logged-in user: {request.user}')
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
        total_spent = budget.get_total_expenses()
        remaining = budget.remaining_amount()
        
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




