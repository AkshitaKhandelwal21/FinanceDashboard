# Generated by Django 4.2.3 on 2024-10-22 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fin', '0003_alter_budget_unique_together_alter_budget_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budgets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Rent', 'Rent'), ('Entertainment', 'Entertainment'), ('Transportation', 'Transportation'), ('Savings', 'Savings'), ('Other', 'Other')], max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adjusted_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('recurring', models.BooleanField(default=False)),
                ('notification_threshold', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category', 'month', 'year')},
            },
        ),
        migrations.DeleteModel(
            name='Budget',
        ),
    ]
