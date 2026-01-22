from django.db import models


class DeliveryTour(models.Model):
    STATUS_CHOICES = [('planned', 'Planned'),('in_progress', 'In Progress'),('completed', 'Completed'),('cancelled', 'Cancelled'),]

    driver = models.ForeignKey('Drivers.Driver', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicles.Vehicle', on_delete=models.CASCADE)
    shipments = models.ManyToManyField('Shipment.Shipment')
    tour_number = models.CharField(max_length=20, unique=True)
    tour_distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # en km
    tour_duration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # en heures
    tour_fuel_consumption = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # en litres
    tour_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planned') 
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Tour #{self.tour_number} - {self.driver.driver_name}"