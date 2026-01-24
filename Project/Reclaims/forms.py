from django import forms
from .models import Reclaim, Reclaim_Packages, Reclaim_Invoice
from Package.models import Package
from Invoice.models import Invoice

class ReclaimForm(forms.ModelForm):
    # Multi-select fields for related packages & invoices
    packages = forms.ModelMultipleChoiceField(
        queryset=Package.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select packages associated with this reclaim"
    )

    invoices = forms.ModelMultipleChoiceField(
        queryset=Invoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select invoices associated with this reclaim"
    )

    class Meta:
        model = Reclaim
        fields = [
            'reclaim_number',
            'reclaim_type',
            'reclaim_description',
            'reclaim_priority',
            'reclaim_status',
            'reclaim_date',
            'reclaim_resolution_date',
            'agent',
        ]
        widgets = {
            'reclaim_description': forms.Textarea(attrs={'class': 'auto-textarea', 'placeholder': 'Describe the issue...'}),
            'reclaim_date': forms.DateInput(attrs={'type': 'date'}),
            'reclaim_resolution_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-select related packages/invoices if editing an existing reclaim
        if self.instance.pk:
            self.fields['packages'].initial = Reclaim_Packages.objects.filter(
                reclaim=self.instance
            ).values_list('package_id', flat=True)
            self.fields['invoices'].initial = Reclaim_Invoice.objects.filter(
                reclaim=self.instance
            ).values_list('invoice_id', flat=True)

    def save(self, commit=True):
        reclaim = super().save(commit=commit)

        # Update related packages
        selected_packages = self.cleaned_data.get('packages', [])
        # Remove any packages not selected
        Reclaim_Packages.objects.filter(reclaim=reclaim).exclude(package__in=selected_packages).delete()
        # Add selected packages
        for package in selected_packages:
            Reclaim_Packages.objects.get_or_create(reclaim=reclaim, package=package)

        # Update related invoices
        selected_invoices = self.cleaned_data.get('invoices', [])
        Reclaim_Invoice.objects.filter(reclaim=reclaim).exclude(invoice__in=selected_invoices).delete()
        for invoice in selected_invoices:
            Reclaim_Invoice.objects.get_or_create(reclaim=reclaim, invoice=invoice)

        return reclaim
