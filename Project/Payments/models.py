# payments/models.py
from django.db import models
from django.utils import timezone

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit Card'),
        ('transfer', 'Bank Transfer'),
        ('check', 'Check'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Relations
    invoice = models.ForeignKey('Invoice.Invoice', on_delete=models.CASCADE)
    
    # Payment information
    payment_number = models.CharField(max_length=20, unique=True)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='completed')
    
    # System fields
    payment_created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment #{self.payment_number} - {self.payment_amount} DZD"
    
    def save(self, *args, **kwargs):
        if not self.payment_number:
            import random
            import string
            self.payment_number = 'PAY' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)