from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    is_predefined = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='expenses'
    )
    description = models.TextField(
        max_length=500,
        blank=True
    )
    date = models.DateField(
        default=timezone.now
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f"{self.amount} - {self.category} on {self.date}"
