from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'client', 'shipments', 'due_date', 'tax_rate', 'status', 'notes'
        ]
