from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('add/', views.student_add, name='student_add'),
    path('<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/add/', views.class_add, name='class_add'),
    path('departments/', views.department_list, name='department_list'),
]
