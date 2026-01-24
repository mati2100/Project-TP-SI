from decimal import Decimal
from django.db import models
from django.db.models import F

from Shipment.models import Shipment


class Invoice(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'),('Paid', 'Paid'),('Partially Paid', 'Partially Paid'),('Overdue', 'Overdue'),]

    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_issue_date = models.DateField()
    invoice_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    invoice_created_at = models.DateTimeField(auto_now_add=True)
    #foriegn keys
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)

    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.client.client_lastname} {self.client.client_firstname}"
    
    def get_shipments(self):
        return Shipment.objects.filter(invoice=self)

    # Override save method to calculate total amount needs update
    def save(self, *args, **kwargs):
        self.invoice_tax_amount = self.invoice_subtotal * Decimal('0.19')  # Assuming a fixed tax rate of 19%
        self.invoice_total_amount = self.invoice_subtotal + self.invoice_tax_amount

    # Add Invoice amount to client balance
        self.client.client_due_balance = F('client_due_balance') + self.invoice_total_amount
        self.client.save(update_fields=['client_due_balance'])

        super().save(*args, **kwargs)

    def get_shipments(self):
        return Shipment.objects.filter(invoice=self)