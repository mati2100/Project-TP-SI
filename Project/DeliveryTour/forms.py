from django import forms
from .models import DeliveryTour

class DeliveryTourForm(forms.ModelForm):
    class Meta:
        model = DeliveryTour
        fields = [
            'driver', 'vehicle', 'shipments', 'tour_number',
            'date', 'distance', 'duration', 'fuel_consumption',
            'status', 'total_weight', 'total_volume'
        ]
