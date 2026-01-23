from django.db import models


class Package(models.Model):
    package_weight = models.DecimalField(max_digits=10, decimal_places=2)
    package_volume = models.CharField(max_length=100)
    package_description = models.TextField()
    package_value = models.DecimalField(max_digits=10, decimal_places=2)

    package_created_at = models.DateTimeField(auto_now_add=True)

    #foreign keys
    shipment = models.ForeignKey('Shipment.Shipment', on_delete=models.CASCADE, related_name='packages')

    def __str__(self):
        return f"Package #{self.id} - {self.package_description[:20]}"