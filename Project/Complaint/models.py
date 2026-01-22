from django.db import models

class Complaint(models.Model):
    STATUS_CHOICES = [('open', 'Open'),('in_progress', 'In Progress'),('resolved', 'Resolved'),('closed', 'Closed'),]
    PRIORITY_CHOICES = [('high', 'High'),('medium', 'Medium'),('low', 'Low'),]
    CATEGORY_CHOICES = [('delivery', 'Delivery Issue'),('billing', 'Billing Issue'),('service', 'Service Quality'),('damage', 'Damaged Goods'),('delay', 'Delivery Delay'),('other', 'Other'),]

    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    shipment = models.ForeignKey('Shipment.Shipment', on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey('Invoice.Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    complaint_number = models.CharField(max_length=20, unique=True)
    complaint_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    complaint_description = models.TextField()
    complaint_date = models.DateField(auto_now_add=True)
    complaint_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    complaint_priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES,default='low') 
    
    def __str__(self):
        return f"Complaint #{self.complaint_number} - {self.client.client_familyname} {self.client.client_firstname}"