from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from Profiles.decorators import token_required
from Shipment.models import Shipment

@token_required
def index(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=29)

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
        'chart_data': data
    }

    return render(request, "dashboard/index.html", context)
