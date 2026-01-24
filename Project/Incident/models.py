from django.db import models

class Incident(models.Model):
    SEVERITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')]
    TYPE_CHOICES = [('Damage', 'Damage'), ('Delay', 'Delay'), ('Lost', 'Lost'), ('Theft', 'Theft'), ('Address Issue', 'Address Issue'), ('System Error', 'System Error'), ('Other', 'Other'),]

    incident_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    incident_severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='medium')
    incident_description = models.TextField()
    incident_time = models.DateTimeField()

    incident_created_at = models.DateTimeField(auto_now_add=True)
    #foriegn keys
    shipment = models.ForeignKey('Shipment.Shipment', on_delete=models.CASCADE)

    def __str__(self):
        return f"Incident - {self.incident_type} - {self.incident_time}"