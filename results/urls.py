from django.urls import path
from . import views

urlpatterns = [
    path('', views.results_dashboard, name='results_dashboard'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.exam_add, name='exam_add'),
    path('exams/<int:exam_id>/marks/', views.enter_marks, name='enter_marks'),
    path('report/', views.result_report, name='result_report'),
    path('practical/', views.practical_marks, name='practical_marks'),
]
