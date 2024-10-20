from django import forms
from .models import Expense, Income

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'category', 'date', 'description']
