from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('collect/', views.collect_fee, name='collect_fee'),
    path('receipt/<int:pk>/', views.view_receipt, name='view_receipt'),
    path('report/', views.fee_report, name='fee_report'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('structures/', views.fee_structure_list, name='fee_structure_list'),
    path('structures/add/', views.fee_structure_add, name='fee_structure_add'),
    path('scholarships/', views.scholarship_list, name='scholarship_list'),
]
