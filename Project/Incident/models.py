from django.db import models

class Incident(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('paid', 'Paid'),('partially_paid', 'Partially Paid'),('overdue', 'Overdue'),('cancelled', 'Cancelled'),]

    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_issue_date = models.DateField()
    invoice_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    invoice_created_at = models.DateTimeField(auto_now_add=True)
    #foriegn keys
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"Incident - {self.invoice_number} - {self.invoice_issue_date}"