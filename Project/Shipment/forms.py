from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'client', 'service_type', 'destination', 'driver', 'vehicle','shipment_number',
            'shipment_weight', 'shipment_volume', 'shipment_description', 'shipment_status', 'shipment_delivery_date'
        ]
