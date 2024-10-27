from django.db import models
from django.utils import timezone
from decimal import Decimal


# Create your models here.

class InventoryItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_days = models.IntegerField()

class Item(models.Model):
    name = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Preparing', 'Preparing'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Preparing')
    created_at = models.DateTimeField(default=timezone.now)  # Correctly set default

    def __str__(self):
        return f"Order {self.id} - {self.item.name}"

    class Meta:
        ordering = ['-created_at']