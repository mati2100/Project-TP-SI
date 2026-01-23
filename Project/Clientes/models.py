from django.db import models
from django.utils import timezone

class Client(models.Model):
    client_lastname = models.CharField(max_length=100, verbose_name="Last Name")
    client_firstname = models.CharField(max_length=100, verbose_name="First Name")
    client_email = models.EmailField(verbose_name="Email Address",unique=True)
    client_phone = models.CharField(max_length=20, verbose_name="Phone Number")
    client_address = models.TextField(verbose_name="Full Address")
    client_city = models.CharField(max_length=100, verbose_name="City")
    client_country = models.CharField(max_length=100, verbose_name="Country", default="Algeria")
    client_registration_date = models.DateTimeField(auto_now_add=True)
    client_actif = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.client_lastname} {self.client_firstname} - {'Active' if self.client_actif else 'Inactive'}"

    # Méthode pour récupérer les expéditions du client
    def get_shipments(self):
        from Shipment.models import Shipment
        return Shipment.objects.filter(client=self)
    
    # Méthode pour récupérer les factures du client
    def get_invoices(self):
        from Invoice.models import Invoice
        return Invoice.objects.filter(client=self)
    
    # Méthode pour récupérer les réclamations du client
    def get_complaints(self):
        from Complaint.models import Complaint
        return Complaint.objects.filter(client=self)