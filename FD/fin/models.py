from django.db import models
from django.contrib.auth.models import User

# Category choices for income and expenses
EXPENSE_CATEGORIES = [
    ('Food', 'Food'),
    ('Transport', 'Transport'),
    ('Rent', 'Rent'),
    ('Entertainment', 'Entertainment'),
    ('Gifts', 'Gifts'),
    ('Bills', 'Bills'),
    ('Other', 'Other'),
]

INCOME_CATEGORIES = [
    ('Salary', 'Salary'),
    ('Freelance', 'Freelance'),
    ('Investments', 'Investments'),
    ('Gifts', 'Gifts'),
    ('Other', 'Other'),
]

# Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount}'

# Income Model
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=INCOME_CATEGORIES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount}'

