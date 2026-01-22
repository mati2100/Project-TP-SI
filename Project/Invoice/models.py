from django.db import models

class Invoice(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('paid', 'Paid'),('partially_paid', 'Partially Paid'),('overdue', 'Overdue'),('cancelled', 'Cancelled'),]

    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    shipments = models.ManyToManyField('Shipment.Shipment')
    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_issue_date = models.DateField(auto_now_add=True)
    invoice_due_date = models.DateField(null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    invoice_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.client.client_familyname} {self.client.client_firstname}"
    
    def calculate_amounts(self):
        subtotal = sum(shipment.estimated_amount for shipment in self.shipments.all())
        self.subtotal = subtotal
        self.tax_amount = subtotal * 0.19
        self.total_amount = subtotal + self.tax_amount
        self.balance_due = self.total_amount - self.amount_paid
        self.save()