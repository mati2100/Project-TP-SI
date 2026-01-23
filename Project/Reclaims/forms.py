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
