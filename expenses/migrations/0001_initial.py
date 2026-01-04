import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_predefined', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, help_text='Leave blank for predefined categories, set for custom user categories', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount in your currency', max_digits=10)),
                ('description', models.TextField(blank=True, help_text='Optional description of the expense', max_length=500)),
                ('date', models.DateField(default=django.utils.timezone.now, help_text='Date of the expense')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expenses', to='expenses.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
                'indexes': [models.Index(fields=['user', 'date'], name='expenses_ex_user_id_713a9d_idx'), models.Index(fields=['user', 'category'], name='expenses_ex_user_id_45749f_idx')],
            },
        ),
    ]
