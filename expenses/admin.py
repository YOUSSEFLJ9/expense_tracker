from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_predefined', 'created_at']
    list_filter = ['is_predefined', 'created_at']
    search_fields = ['name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'category', 'date', 'created_at']
    list_filter = ['category', 'date', 'created_at']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'date'
