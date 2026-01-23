from django.db import models

class Incident(models.Model):
    TYPE_CHOICES = [('delay', 'Delay'),('loss', 'Loss'),('damage', 'Damage'),('technical', 'Technical Issue'),('accident', 'Accident'),('other', 'Other'),]
    SEVERITY_CHOICES = [('low', 'Low'),('medium', 'Medium'),('high', 'High'),('critical', 'Critical'),]

    shipment = models.ForeignKey('Shipment.Shipment', on_delete=models.CASCADE)
    tour = models.ForeignKey('Package.Package', on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    incident_severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='medium')
    incident_description = models.TextField()
    incident_location = models.CharField(max_length=200, blank=True)
    incident_date = models.DateTimeField()
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Incident - {self.get_incident_type_display()} - {self.incident_date}"