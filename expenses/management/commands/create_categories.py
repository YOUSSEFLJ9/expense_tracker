from django.core.management.base import BaseCommand
from expenses.models import Category


class Command(BaseCommand):
    help = 'Create predefined expense categories'

    def handle(self, *args, **kwargs):
        predefined_categories = [
            'Food',
            'Transport',
            'Rent',
            'Entertainment',
            'Health',
            'Shopping',
            'Utilities',
            'Education',
            'Other',
        ]

        created_count = 0
        for category_name in predefined_categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                user=None,
                defaults={'is_predefined': True}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} new predefined categories!'
            )
        )
