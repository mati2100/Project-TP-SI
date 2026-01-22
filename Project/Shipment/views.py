from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from Profiles.decorators import token_required


@token_required
def ShipmentListView(request):
    shipments = Shipment.objects.all()
    return render(request, 'shipment_list.html', {'shipments': shipments})

@token_required
def ShipmentCreateView(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shipment_list')
    else:
        form = ShipmentForm()
    
    return render(request, 'shipment_form.html', {
        'form': form,
        'title': 'Create New Shipment'
    })

@token_required
def ShipmentUpdateView(request, shipment_id):
    shipment = Shipment.objects.get(id=shipment_id)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect('shipment_list')
    else:
        form = ShipmentForm(instance=shipment)
    
    return render(request, 'shipment_form.html', {
        'form': form,
        'title': 'Update Shipment',
        'shipment': shipment
    })

@token_required
def ShipmentDeleteView(request, shipment_id):
    shipment = Shipment.objects.get(id=shipment_id)
    
    if request.method == 'POST':
        shipment.delete()
        return redirect('shipment_list')
    
    return render(request, 'shipment_confirm_delete.html', {'shipment': shipment})