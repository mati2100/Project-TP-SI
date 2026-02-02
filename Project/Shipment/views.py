from django.shortcuts import render, redirect
from django.db import models
from django.urls import reverse
from .models import Shipment
from .forms import ShipmentForm
from Profiles.decorators import token_required


@token_required
def ShipmentListView(request):
    shipments = Shipment.objects.all()
    
    query = request.GET.get('q')
    search_by = request.GET.get('by')

    if query:
        if search_by == 'number':
            shipments = shipments.filter(shipment_tracking_number__icontains=query)
        elif search_by == 'status':
            shipments = shipments.filter(shipment_status__icontains=query)
        elif search_by == 'client':
            shipments = shipments.filter(client__client_firstname__icontains=query) | shipments.filter(client__client_familyname__icontains=query)
        elif search_by == 'driver':
            shipments = shipments.filter(driver__driver_first_name__icontains=query) | shipments.filter(driver__driver_last_name__icontains=query)

    return render(request, 'shipment_list.html', {'shipments': shipments})

@token_required
def ShipmentCreateView(request):
    form = ShipmentForm(request.POST or None)

    #Adds create new links to foreign key fields
    for name, field in form.fields.items():
        try:
            model_field = form._meta.model._meta.get_field(name)
        except:
            continue

        if isinstance(model_field, models.ForeignKey):
            try:
                url_name = f"{model_field.related_model._meta.model_name}_create"
                create_url = reverse(url_name)
                next_url = request.path
                field.help_text = (
                    f'<a class="add-new-button" href="{create_url}?next={next_url}">+ Add new</a>')
            except:
                pass

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(request.GET.get("next", "shipment_list"))

    return render(request, "shipment_form.html", {
        "form": form,
        "title": "Create Shipment",
    })


@token_required
def ShipmentUpdateView(request, shipment_id):
    shipment = Shipment.objects.get(id=shipment_id)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next", "shipment_list"))
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
        #  Go back to where user came from
        return redirect(request.GET.get("next", "shipment_list"))
    
    return render(request, 'shipment_confirm_delete.html', {'shipment': shipment})