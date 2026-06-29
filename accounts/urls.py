from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.manage_users, name='manage_users'),
    path("assign-subject/", views.assign_subject, name="assign_subject"),
]
