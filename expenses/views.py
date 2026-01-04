from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import csv
import json

from .models import Expense, Category
from .forms import UserRegistrationForm, ExpenseForm, CategoryForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Expense Tracker.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'expenses/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'expenses/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    
    today = timezone.now()
    current_month_start = today.replace(day=1)
    monthly_total = Expense.objects.filter(
        user=user,
        date__gte=current_month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    recent_expenses = Expense.objects.filter(user=user)[:5]
    category_data = Expense.objects.filter(
        user=user,
        date__gte=current_month_start
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    category_labels = [item['category__name'] or 'Uncategorized' for item in category_data]
    category_amounts = [float(item['total']) for item in category_data]
    last_7_days = today - timedelta(days=6)
    daily_data = Expense.objects.filter(
        user=user,
        date__gte=last_7_days
    ).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    daily_dict = {(last_7_days + timedelta(days=i)).date(): 0 for i in range(7)}
    for item in daily_data:
        daily_dict[item['date']] = float(item['total'])
    
    daily_labels = [date.strftime('%b %d') for date in sorted(daily_dict.keys())]
    daily_amounts = [daily_dict[date] for date in sorted(daily_dict.keys())]
    
    context = {
        'monthly_total': monthly_total,
        'total_expenses': total_expenses,
        'recent_expenses': recent_expenses,
        'category_labels': json.dumps(category_labels),
        'category_amounts': json.dumps(category_amounts),
        'daily_labels': json.dumps(daily_labels),
        'daily_amounts': json.dumps(daily_amounts),
    }
    
    return render(request, 'expenses/dashboard.html', context)


@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user)
    
    category_filter = request.GET.get('category')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)
    
    if month_filter and year_filter:
        expenses = expenses.filter(
            date__month=month_filter,
            date__year=year_filter
        )
    
    categories = Category.objects.filter(
        Q(is_predefined=True) | Q(user=request.user)
    )
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'total': total,
        'selected_category': category_filter,
        'selected_month': month_filter,
        'selected_year': year_filter,
    }
    
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_create_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
    
    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'title': 'Add Expense'
    })


@login_required
def expense_update_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    
    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'title': 'Edit Expense',
        'expense': expense
    })


@login_required
def expense_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    
    return render(request, 'expenses/expense_confirm_delete.html', {
        'expense': expense
    })


@login_required
def category_list_view(request):
    predefined_categories = Category.objects.filter(is_predefined=True)
    custom_categories = Category.objects.filter(user=request.user)
    
    context = {
        'predefined_categories': predefined_categories,
        'custom_categories': custom_categories,
    }
    
    return render(request, 'expenses/category_list.html', context)


@login_required
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.is_predefined = False
            try:
                category.save()
                messages.success(request, 'Category created successfully!')
                return redirect('category_list')
            except:
                messages.error(request, 'A category with this name already exists.')
    else:
        form = CategoryForm()
    
    return render(request, 'expenses/category_form.html', {
        'form': form,
        'title': 'Add Custom Category'
    })


@login_required
def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'expenses/category_confirm_delete.html', {
        'category': category
    })


@login_required
def monthly_report_view(request):
    today = timezone.now()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    
    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )
    
    monthly_total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    category_breakdown = expenses.values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="expenses_{year}_{month}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Category', 'Description', 'Amount'])
        
        for expense in expenses:
            writer.writerow([
                expense.date,
                expense.category.name if expense.category else 'Uncategorized',
                expense.description,
                expense.amount
            ])
        
        writer.writerow([])
        writer.writerow(['Total', '', '', monthly_total])
        
        return response
    
    years = range(today.year - 5, today.year + 1)
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    average_expense = 0
    if expenses.count() > 0:
        average_expense = monthly_total / expenses.count()
    
    context = {
        'expenses': expenses,
        'monthly_total': monthly_total,
        'category_breakdown': category_breakdown,
        'selected_month': month,
        'selected_year': year,
        'years': years,
        'months': months,
        'average_expense': average_expense,
    }
    
    return render(request, 'expenses/monthly_report.html', context)
