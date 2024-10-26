from django import forms
from django.utils import timezone
from .models import Expense, Income, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'category', 'date', 'description']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year', 'recurring', 'notification_threshold']
        widgets = {
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'min': 2020, 'max': 2100}),
            'amount': forms.NumberInput(attrs={'step': 0.01}),
            'adjusted_amount': forms.NumberInput(attrs={'step': 0.01}),
            'notification_threshold': forms.NumberInput(attrs={'step': 0.01}),
        }
