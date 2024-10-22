from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum


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

CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Entertainment', 'Entertainment'),
        ('Transportation', 'Transportation'),
        ('Savings', 'Savings'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

# Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES)
    date = models.DateField(default=timezone.now)
    month = models.IntegerField()
    year = models.IntegerField() 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount} on {self.date}'

# Income Model
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=INCOME_CATEGORIES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount}'

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link budget to a user
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  # Category
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Initial Budget
    # adjusted_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Adjusted budget after updates
    month = models.IntegerField()  # Month (1-12)
    year = models.IntegerField()  # Year
    recurring = models.BooleanField(default=False)  # Recurring budget (yes/no)
    notification_threshold = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Aler

    def remaining_amount(self):
        # Calculate remaining amount based on expenses
        total_spent = self.get_total_expenses()
        remaining = self.amount - total_spent
        return remaining

    def get_total_expenses(self):
        # Summarize expenses for this budget category
        total = Expense.objects.filter(user=self.user, category=self.category, month=self.month, year=self.year).aggregate(Sum('amount'))['amount__sum'] or 0
        return total

    # def get_total_expenses(self):
    #     total = sum([Expense.amount for Expense in self.Expense.all()])  # Make sure expense.amount is a number
    #     return total

    def __str__(self):
        return f'{self.category} - {self.amount} for {self.month}/{self.year}'
    
    class Meta:
        unique_together = ('user', 'category', 'month', 'year')