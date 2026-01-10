from django.db import models

class Invoice(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('paid', 'Paid'),('partially_paid', 'Partially Paid'),('overdue', 'Overdue'),('cancelled', 'Cancelled'),]
    
    # Relations
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    shipments = models.ManyToManyField('Shipment.Shipment')
    
    # Informations de facturation
    invoice_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    # Montants
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)  # TVA 19%
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Statut
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.client.client_nom}"
    
    def calculate_amounts(self):
        # Calculer le sous-total à partir des expéditions
        subtotal = sum(shipment.estimated_amount for shipment in self.shipments.all())
        self.subtotal = subtotal
        self.tax_amount = subtotal * (self.tax_rate / 100)
        self.total_amount = subtotal + self.tax_amount
        self.balance_due = self.total_amount - self.amount_paid
        self.save()