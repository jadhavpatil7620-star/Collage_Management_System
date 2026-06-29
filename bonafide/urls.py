from django.urls import path
from . import views

urlpatterns = [
    path('', views.bonafide_list, name='bonafide_list'),
    path('issue/', views.issue_bonafide, name='issue_bonafide'),
    path('print/<int:pk>/', views.print_bonafide, name='print_bonafide'),
    path('leaving/', views.leaving_cert_list, name='leaving_cert_list'),
    path('leaving/issue/', views.issue_leaving_cert, name='issue_leaving_cert'),
    path('leaving/print/<int:pk>/', views.print_leaving_cert, name='print_leaving_cert'),
]
