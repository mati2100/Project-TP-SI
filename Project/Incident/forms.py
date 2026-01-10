from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'shipment', 'tour', 'incident_type', 'severity',
            'description', 'location', 'incident_date',
            'is_resolved', 'resolution_notes'
        ]