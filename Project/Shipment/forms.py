from django.utils import timezone
import uuid
from django import forms
from .models import Shipment
from Package.models import Package

class ShipmentForm(forms.ModelForm):
    packages = forms.ModelMultipleChoiceField(
        queryset=Package.objects.filter(shipment__isnull=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select packages to include in this shipment"
    )
    class Meta:
        model = Shipment
        fields = [
            'client',
            'destination',
            'vehicle',
            'driver',
            'shipment_tracking_number',
            'shipment_status',
            'shipment_expected_delivery_date',
            'shipment_delivery_date',
            'shipment_notes',
            'service_type',
            'invoice',
            'shipment_total_weight',
            'shipment_total_volume',
        ]

    # Override save method to handle one-to-many relationship for packages
    def save(self, commit=True):
        shipment = super().save(commit=False)

        if commit:
            shipment.save()

        selected_packages = self.cleaned_data['packages']
        selected_packages.update(shipment=shipment)

        shipment.calculate_totals()

        return shipment

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        #
        self.fields["client"].help_text = ('<a href="{% url \'client_create\' %}?next={{ request.path }}">➕ Add new client</a>')

        # empty labels placeholders
        self.fields['client'].empty_label = "Please Select a Client"
        self.fields['destination'].empty_label = "No destination assigned"
        self.fields['driver'].empty_label = "No driver assigned"
        self.fields['vehicle'].empty_label = "No vehicle assigned"
        self.fields['service_type'].empty_label = "No service type assigned"
        self.fields['invoice'].empty_label = "No invoice yet"

        # field foreign keys formators
        self.fields['client'].label_from_instance = lambda obj: f"{obj.client_firstname} - {obj.client_lastname} (#{obj.id})"
        self.fields['destination'].label_from_instance = lambda obj: f"{obj.destination_city} - {obj.destination_state} - {obj.destination_country} (#{obj.id})"
        self.fields['driver'].label_from_instance = lambda obj: f"{obj.driver_last_name} {obj.driver_first_name} (#{obj.id})"
        self.fields['vehicle'].label_from_instance = lambda obj: f"{obj.vehicle_registration_number} - {obj.vehicle_model} - {obj.vehicle_brand} (#{obj.id})"
        self.fields['service_type'].label_from_instance = lambda obj: f"{obj.service_type_name} - {obj.service_type_priority_level} (#{obj.id})"
        self.fields['invoice'].label_from_instance = lambda obj: f"Invoice #{obj.id} - Amount: {obj.invoice_total_amount} (#{obj.id})"

        # make total weight and total volume read-only
        self.fields['shipment_total_weight'].widget.attrs['readonly'] = True
        self.fields['shipment_total_volume'].widget.attrs['readonly'] = True

        # generate tracking number for new shipments
        if not self.instance.pk:
            today = timezone.now().strftime("%Y%m%d")
            random_part = uuid.uuid4().hex[:6].upper()
            self.fields['shipment_tracking_number'].initial = f"SHP-{today}-{random_part}"