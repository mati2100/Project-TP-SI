from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'client', 'service_type', 'destination', 'driver', 'vehicle',
            'weight', 'volume', 'description', 'status', 'delivery_date'
        ]
