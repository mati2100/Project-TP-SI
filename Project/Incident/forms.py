from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'invoice_number', 
            'invoice_issue_date', 
            'invoice_subtotal', 
            'invoice_tax_amount',
            'invoice_status',
            'client',
        ]