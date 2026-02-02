from django.db import models


class Reclaim(models.Model):
    STATUS_CHOICES = [('open', 'Open'),('in_progress', 'In Progress'),('resolved', 'Resolved'),('closed', 'Closed'),]
    PRIORITY_CHOICES = [('high', 'High'),('medium', 'Medium'),('low', 'Low'),]
    CATEGORY_CHOICES = [('delivery', 'Delivery Issue'),('billing', 'Billing Issue'),('service', 'Service Quality'),('damage', 'Damaged Goods'),('delay', 'Delivery Delay'),('other', 'Other'),]

    reclaim_number = models.CharField(max_length=20, unique=True)
    reclaim_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    reclaim_description = models.TextField()
    reclaim_date = models.DateField()
    reclaim_resolution_date = models.DateField(null=True, blank=True)
    reclaim_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    reclaim_priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES,default='low') 

    reclaim_created_at = models.DateTimeField(auto_now_add=True)

    #foreign keys
    agent = models.ForeignKey('Profiles.Agent', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Reclaim #{self.reclaim_number} - {self.client.client_lastname} {self.client.client_firstname}"
    
    def packages_affected(self):
        return ", ".join([str(rp.package) for rp in self.reclaim_packages_set.all()])
    
    def invoices_affected(self):
        return ", ".join([str(ri.invoice) for ri in self.reclaim_invoice_set.all()])
    
class Reclaim_Packages(models.Model):
    
    reclaim_packages_created_at = models.DateTimeField(auto_now_add=True)

    #foreign keys
    reclaim = models.ForeignKey('Reclaims.Reclaim', on_delete=models.CASCADE)
    package = models.ForeignKey('Package.Package', on_delete=models.CASCADE)

    def __str__(self):  
        return f"Reclaim #{self.reclaim.reclaim_number} - Package #{self.package.id}"

class Reclaim_Invoice(models.Model):
    reclaim_invoice_created_at = models.DateTimeField(auto_now_add=True)

    #foreign keys
    reclaim = models.ForeignKey('Reclaims.Reclaim', on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice.Invoice', on_delete=models.CASCADE)

    def __str__(self):  
        return f"Reclaim #{self.reclaim.reclaim_number} - Invoice #{self.invoice.invoice_number}"