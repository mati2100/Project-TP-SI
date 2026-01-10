from django.db import models

class Driver(models.Model):
    driver_name = models.CharField(max_length=100)
    driver_email = models.EmailField(unique=True)
    driver_phone = models.CharField(max_length=20)
    driver_address = models.TextField()
    driver_license = models.CharField(max_length=50, unique=True)
    license_type = models.CharField(max_length=50)
    driver_active = models.BooleanField(default=True)
    driver_available = models.BooleanField(default=True)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.driver_name} ({self.driver_license})"
    
    # Méthode pour récupérer les expéditions du client
    def get_shipments(self):
        from Shipment_app.models import Shipment
        return Shipment.objects.filter(client=self)
    
    # Méthode pour récupérer les factures du client
    def get_invoices(self):
        from Invoice_app.models import Invoice
        return Invoice.objects.filter(client=self)
    
    # Méthode pour récupérer les réclamations du client
    def get_complaints(self):
        from Complaint.models import Complaint
        return Complaint.objects.filter(client=self)