from django.contrib import admin
from .models import Expense, Income

# Registering the models to make them accessible via the admin interface
admin.site.register(Expense)
admin.site.register(Income)