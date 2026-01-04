from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Category, Expense
from datetime import datetime, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create sample data for testing and demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='demo',
            help='Username for the demo account (default: demo)'
        )

    def handle(self, *args, **kwargs):
        username = kwargs['username']

        self.stdout.write('Creating demo user...')
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Demo user created: {username}'))
            self.stdout.write(self.style.SUCCESS(f'   Password: demo1234'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  User {username} already exists'))

        categories = list(Category.objects.filter(is_predefined=True))
        
        if not categories:
            self.stdout.write(self.style.ERROR('❌ No predefined categories found!'))
            self.stdout.write('   Run: python manage.py create_categories')
            return

        expense_descriptions = {
            'Food': [
                'Grocery shopping at supermarket',
                'Lunch at restaurant',
                'Coffee and snacks',
                'Dinner with friends',
                'Food delivery',
            ],
            'Transport': [
                'Taxi to work',
                'Bus ticket',
                'Gas refill',
                'Uber ride',
                'Parking fee',
            ],
            'Entertainment': [
                'Movie tickets',
                'Concert tickets',
                'Streaming subscription',
                'Video games',
                'Books',
            ],
            'Health': [
                'Pharmacy',
                'Doctor visit',
                'Gym membership',
                'Vitamins and supplements',
                'Medical checkup',
            ],
            'Shopping': [
                'Clothes shopping',
                'Electronics',
                'Home decor',
                'Gifts',
                'Accessories',
            ],
            'Utilities': [
                'Electricity bill',
                'Water bill',
                'Internet bill',
                'Mobile phone bill',
                'Gas bill',
            ],
        }

        self.stdout.write('Creating sample expenses...')
        today = datetime.now().date()
        created_count = 0

        for days_ago in range(60):
            expense_date = today - timedelta(days=days_ago)
            
            num_expenses = random.randint(1, 3)
            
            for _ in range(num_expenses):
                category = random.choice(categories)
                
                if category.name in expense_descriptions:
                    description = random.choice(expense_descriptions[category.name])
                else:
                    description = f'Expense for {category.name}'
                
                amount_ranges = {
                    'Food': (5, 50),
                    'Transport': (3, 30),
                    'Rent': (500, 1500),
                    'Entertainment': (10, 100),
                    'Health': (20, 200),
                    'Shopping': (15, 150),
                    'Utilities': (30, 150),
                    'Education': (50, 300),
                    'Other': (5, 100),
                }
                
                min_amount, max_amount = amount_ranges.get(category.name, (10, 100))
                amount = Decimal(random.uniform(min_amount, max_amount)).quantize(Decimal('0.01'))
                
                Expense.objects.create(
                    user=user,
                    amount=amount,
                    category=category,
                    description=description,
                    date=expense_date
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {created_count} sample expenses'))
        
        custom_category, created = Category.objects.get_or_create(
            name='Coffee',
            user=user,
            defaults={'is_predefined': False}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created custom category: Coffee'))
            
            for days_ago in range(30, 0, -3):
                expense_date = today - timedelta(days=days_ago)
                Expense.objects.create(
                    user=user,
                    amount=Decimal(random.uniform(3, 8)).quantize(Decimal('0.01')),
                    category=custom_category,
                    description=random.choice([
                        'Morning coffee',
                        'Afternoon latte',
                        'Coffee with colleague',
                        'Cappuccino',
                    ]),
                    date=expense_date
                )

        total_expenses = Expense.objects.filter(user=user).count()
        total_amount = Expense.objects.filter(user=user).aggregate(
            total=Sum('amount')
        )['total'] or 0

        from django.db.models import Sum

        total_amount = Expense.objects.filter(user=user).aggregate(
            total=Sum('amount')
        )['total'] or 0

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('  Demo Data Created Successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Password: demo1234')
        self.stdout.write(f'  Total Expenses: {total_expenses}')
        self.stdout.write(f'  Total Amount: ${total_amount:.2f}')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('You can now login and explore the application!')
