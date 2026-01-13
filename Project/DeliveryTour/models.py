from django.db import models

class DeliveryTour(models.Model):
    STATUS_CHOICES = [('planned', 'Planned'),('in_progress', 'In Progress'),('completed', 'Completed'),('cancelled', 'Cancelled'),]
    
    # Relations
    driver = models.ForeignKey('Drivers.Driver', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicles.Vehicle', on_delete=models.CASCADE)
    shipments = models.ManyToManyField('Shipment.Shipment')
    
    # Informations de la tournée
    tour_number = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # en km
    duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # en heures
    fuel_consumption = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # en litres
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planned')
    
    # Statistiques
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed_shipments = models.IntegerField(default=0)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Tour #{self.tour_number} - {self.driver.driver_name}"