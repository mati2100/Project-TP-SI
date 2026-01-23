from django.db import models
from django.db.models import F


class Invoice(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('paid', 'Paid'),('partially_paid', 'Partially Paid'),('overdue', 'Overdue'),]

    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_issue_date = models.DateField()
    invoice_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=19)
    invoice_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    invoice_created_at = models.DateTimeField(auto_now_add=True)
    #foriegn keys
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)

    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.client.client_familyname} {self.client.client_firstname}"
    
    # Override save method to calculate total amount needs update
    def save(self, *args, **kwargs):
        self.invoice_total_amount = F('invoice_subtotal') + F('invoice_tax_amount')
        super().save(*args, **kwargs)