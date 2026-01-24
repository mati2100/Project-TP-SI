from django import forms
from .models import Reclaim

class ReclaimForm(forms.ModelForm):
    class Meta:
        model = Reclaim
        fields = [
            'reclaim_number',
            'reclaim_type', 
            'reclaim_description',
            'reclaim_date', 
            'reclaim_resolution_date',
            'reclaim_status',
            'reclaim_priority',
            'agent',
        ]
        
        labels = {
            'reclaim_number': 'Reclamation Number',
            'reclaim_type': 'Reclamation Type',
            'reclaim_description': 'Reclamation Description',
            'reclaim_date': 'Date Filed',
            'reclaim_resolution_date': 'Target Resolution',
            'reclaim_status': 'Reclamation Status',
            'reclaim_priority': 'Reclamation Priority',
            'agent': 'Assigned To Agent',
        }
        
        widgets = {
            'reclaim_description': forms.Textarea(attrs={'rows': 3}),
            'reclaim_date': forms.DateInput(attrs={'type': 'date'}),
            'reclaim_resolution_date': forms.DateInput(attrs={'type': 'date'}),
        }