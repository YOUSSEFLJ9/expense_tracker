from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.dashboard_view, name='dashboard'),
    
    path('expenses/', views.expense_list_view, name='expense_list'),
    path('expenses/add/', views.expense_create_view, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_update_view, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete_view, name='expense_delete'),
    
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/add/', views.category_create_view, name='category_create'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category_delete'),
    
    path('reports/monthly/', views.monthly_report_view, name='monthly_report'),
]
