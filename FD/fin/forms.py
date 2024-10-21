from django import forms
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
        fields = ['amount', 'category', 'month', 'year']
        widgets = {
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'min': timezone.now().year}),
        }
