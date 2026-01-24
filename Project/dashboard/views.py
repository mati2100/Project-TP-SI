from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from Profiles.decorators import token_required
from Incident.models import Incident
from Reclaims.models import Reclaim
from Shipment.models import Shipment
from Clientes.models import Client

@token_required
def index(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=29)

    shipments_count = Shipment.objects.count()
    clients_count = Client.objects.count()
    incidents_count = Incident.objects.count()
    reclaims_count = Reclaim.objects.count()
    delivery_data = [Shipment.objects.filter(shipment_status='delivered').count()
                     ,Shipment.objects.filter(shipment_status='delayed').count()
                     ,Shipment.objects.filter(shipment_status='in_transit').count()
                     ,Shipment.objects.filter(shipment_status='cancelled').count()]

    if shipments_count:
        success_rate = round(100 - (reclaims_count / shipments_count) * 100)
    else:
        success_rate = 100

    shipments_per_day = (
        Shipment.objects
        .filter(shipment_created_at__date__gte=start_date)
        .extra(select={'day': "date(shipment_created_at)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    labels = []
    data = []
    for item in shipments_per_day:
        labels.append(item['day'])
        data.append(item['count'])

    context = {
        'chart_labels': labels,
        'chart_data': data,
        'shipments_count': shipments_count,
        'clients_count': clients_count,
        'incidents_count': incidents_count,
        'reclaims_count': reclaims_count,
        'success_rate': success_rate,
        'delivery_rate': delivery_data,
    }

    return render(request, "dashboard/index.html", context)
