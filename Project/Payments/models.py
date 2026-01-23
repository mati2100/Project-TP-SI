from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.db.models import F
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [('cash', 'Cash'),('card', 'Credit Card'),('transfer', 'Bank Transfer'),('check', 'Check'),]
    STATUS_CHOICES = [('pending', 'Pending'),('completed', 'Completed'),('failed', 'Failed'),('refunded', 'Refunded'),]

    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=20, unique=True)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='completed')
    
    def __str__(self):
        return f"Payment #{self.payment_number} - {self.payment_amount} DZD"
    
    def discount_balance(self):
        from Clientes.models import Client
        if self.payment_amount > self.client.balance:
            raise ValidationError("The payment amount exceeds the client's balance.")
    
        Client.objects.filter(id=self.client.id).update(
        client_due_balance=F('client_due_balance') - self.payment_amount
      )