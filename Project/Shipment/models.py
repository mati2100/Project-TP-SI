from django.db import models
from django.utils import timezone

class Shipment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('in_transit', 'In Transit'),('at_sorting_center', 'At Sorting Center'),('out_for_delivery', 'Out for Delivery'),('delivered', 'Delivered'),('failed', 'Delivery Failed'),]
    
    # Relations avec autres modèles
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    service_type = models.ForeignKey('Services.ServiceType', on_delete=models.CASCADE)
    destination = models.ForeignKey('Services.Destination', on_delete=models.CASCADE)
    driver = models.ForeignKey('Drivers.Driver', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey('Vehicles.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Informations de l'expédition
    shipment_number = models.CharField(max_length=20, unique=True, editable=False)
    weight = models.DecimalField(max_digits=10, decimal_places=2)  # en kg
    volume = models.DecimalField(max_digits=10, decimal_places=2)  # en m³
    description = models.TextField()
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Shipment #{self.shipment_number} - {self.client.client_nom}"
    
    def save(self, *args, **kwargs):
        if not self.shipment_number:
            # Générer un numéro unique
            import random
            import string
            self.shipment_number = 'SH' + ''.join(random.choices(string.digits, k=8))
        
        # Calculer le montant estimé
        from Services.models import Destination, ServiceType
        try:
            destination = Destination.objects.get(id=self.destination.id)
            service_type = ServiceType.objects.get(id=self.service_type.id)
            self.estimated_amount = (
                destination.base_fare +
                (self.weight * service_type.st_weight_rate) +
                (self.volume * service_type.st_volume_rate)
            )
        except:
            pass
        
        super().save(*args, **kwargs)