from django.db import models

class Complaint(models.Model):
    STATUS_CHOICES = [('open', 'Open'),('in_progress', 'In Progress'),('resolved', 'Resolved'),('closed', 'Closed'),]
    
    CATEGORY_CHOICES = [('delivery', 'Delivery Issue'),('billing', 'Billing Issue'),('service', 'Service Quality'),('damage', 'Damaged Goods'),('delay', 'Delivery Delay'),('other', 'Other'),]
    
    # Relations
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    shipment = models.ForeignKey('Shipment.Shipment', on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey('Invoice.Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey('Profiles.Agent', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Informations sur la réclamation
    complaint_number = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    # Dates
    complaint_date = models.DateField(auto_now_add=True)
    target_resolution_date = models.DateField(null=True, blank=True)
    actual_resolution_date = models.DateField(null=True, blank=True)
    
    # Statut
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    priority = models.IntegerField(default=3)  # 1=High, 2=Medium, 3=Low
    
    def __str__(self):
        return f"Complaint #{self.complaint_number} - {self.client.client_nom}"