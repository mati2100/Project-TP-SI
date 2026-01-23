from django.db import models

class Invoice(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('paid', 'Paid'),('partially_paid', 'Partially Paid'),('overdue', 'Overdue'),('cancelled', 'Cancelled'),]

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
    
    def calculate_amounts(self):
        subtotal = sum(shipment.estimated_amount for shipment in self.shipments.all())
        self.invoice_subtotal = subtotal
        self.invoice_tax_amount = subtotal * 0.19
        self.invoice_total_amount = subtotal + self.invoice_tax_amount
        self.balance_due = self.invoice_total_amount - self.invoice_amount_paid
        self.save()