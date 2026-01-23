from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'shipment_tracking_number',
            'shipment_total_weight',
            'shipment_total_volume',
            'shipment_status',
            'shipment_expected_delivery_date',
            'shipment_delivery_date',
            'shipment_notes',
            'driver',
            'destination',
            'service_type',
            'client',
            'vehicle',
            'invoice',
        ]
