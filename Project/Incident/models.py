from django.db import models

class Incident(models.Model):
    TYPE_CHOICES = [('delay', 'Delay'),('loss', 'Loss'),('damage', 'Damage'),('technical', 'Technical Issue'),('accident', 'Accident'),('other', 'Other'),]
    
    SEVERITY_CHOICES = [('low', 'Low'),('medium', 'Medium'),('high', 'High'),('critical', 'Critical'),]
    
    # Relations
    shipment = models.ForeignKey('Shipment.Shipment', on_delete=models.CASCADE)
    tour = models.ForeignKey('DeliveryTour.DeliveryTour', on_delete=models.CASCADE)
    
    # Informations sur l'incident
    incident_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='medium')
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    
    # Dates
    incident_date = models.DateTimeField()
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Statut
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Incident - {self.get_incident_type_display()} - {self.incident_date}"