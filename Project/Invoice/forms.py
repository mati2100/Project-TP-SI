from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'client', 'shipments', 'invoice_due_date', 'invoice_status', 'invoice_notes'
        ]
