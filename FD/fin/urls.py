from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expense/', views.add_expense, name='add_expense'),
    path('income/', views.add_income, name='add_income'),
    # path('addbudget/', views.add_budget, name='add_budget'),
    # path('editbudget/', views.edit_budget, name='edit_budget'),
    # path('track/', views.budget_tracking, name='budget_tracking')
]   