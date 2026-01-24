from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth
from Profiles.decorators import token_required
from Incident.models import Incident
from Reclaims.models import Reclaim
from Shipment.models import Shipment
from Clientes.models import Client
from Payments.models import Payment
from Package.models import Package
import calendar


@token_required
def index(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=365)

    # Calculate shipment statistics

    shipments_count = Shipment.objects.count()
    clients_count = Client.objects.count()
    incidents_count = Incident.objects.count()
    reclaims_count = Reclaim.objects.count()
    delivery_data = [Shipment.objects.filter(shipment_status='pending').count()
                     ,Shipment.objects.filter(shipment_status='in_transit').count()
                     ,Shipment.objects.filter(shipment_status='at_sorting_center').count()
                     ,Shipment.objects.filter(shipment_status='out_for_delivery').count()
                     ,Shipment.objects.filter(shipment_status='delivered').count()
                     ,Shipment.objects.filter(shipment_status='failed').count()
                     ]

    if shipments_count:
        success_rate = round(100 - (reclaims_count / shipments_count) * 100)
    else:
        success_rate = 100

    #Shipments per month for the last year
    shipments_per_month = (
        Shipment.objects
        .filter(shipment_expected_delivery_date__gte=start_date)
        .annotate(month=TruncMonth('shipment_expected_delivery_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    payments_per_month = (
        Payment.objects
        .filter(payment_date__gte=start_date)
        .annotate(month=TruncMonth('payment_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    packages_per_month = (
        Package.objects
        .filter(shipment__shipment_expected_delivery_date__gte=start_date)
        .annotate(month=TruncMonth('package_created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )


    months, shipments_data = build_monthly_series(shipments_per_month)
    _, payments_data = build_monthly_series(payments_per_month)
    _, packages_data = build_monthly_series(packages_per_month)


    context = {
        'shipments_count': shipments_count,
        'clients_count': clients_count,
        'incidents_count': incidents_count,
        'reclaims_count': reclaims_count,
        'success_rate': success_rate,
        'months': months,
        'shipments_data': shipments_data,
        'payments_data': payments_data,
        'delivery_rate': delivery_data,
        'packages_data': packages_data,
    }


    return render(request, "dashboard/index.html", context)

def build_monthly_series(queryset):
    month_counts = {
        item["month"].month: item["count"]
        for item in queryset
    }

    labels = []
    data = []

    for month in range(1, 13):
        labels.append(calendar.month_name[month])
        data.append(month_counts.get(month, 0))

    return labels, data
