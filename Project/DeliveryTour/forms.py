from django import forms
from .models import DeliveryTour

class DeliveryTourForm(forms.ModelForm):
    class Meta:
        model = DeliveryTour
        fields = [
            'driver', 'vehicle', 'shipments', 'tour_number',
            'tour_distance', 'tour_duration', 'tour_fuel_consumption',
            'tour_status','started_at' ,'completed_at'
        ]
