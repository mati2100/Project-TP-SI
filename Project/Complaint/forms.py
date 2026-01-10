from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'client', 'shipment', 'invoice', 'assigned_to',
            'category', 'description', 'target_resolution_date',
            'status', 'priority'
        ]
