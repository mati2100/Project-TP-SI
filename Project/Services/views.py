from django.shortcuts import render, redirect
from .models import Destination, ServiceType
from .forms import DestinationForm, ServiceTypeForm
from Profiles.decorators import token_required


# Destination Views
@token_required
def DestinationListView(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

@token_required
def DestinationCreateView(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "destination_list"))
    else:
        form = DestinationForm()
    
    return render(request, 'destination_form.html', {
        'form': form,
        'title': 'Create New Destination'
    })

@token_required
def DestinationUpdateView(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "destination_list"))
    else:
        form = DestinationForm(instance=destination)
    
    return render(request, 'destination_form.html', {
        'form': form,
        'title': 'Update Destination',
        'destination': destination
    })
@token_required
def DestinationDeleteView(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    
    if request.method == 'POST':
        destination.delete()
        #  Go back to where user came from
        return redirect(request.GET.get("next", "destination_list"))
    
    return render(request, 'destination_confirm_delete.html', {'destination': destination})

# Service Type Views
@token_required
def ServiceTypeListView(request):
    service_types = ServiceType.objects.all()
    return render(request, 'servicetype_list.html', {'service_types': service_types})

@token_required
def ServiceTypeCreateView(request):
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "servicetype_list"))
    else:
        form = ServiceTypeForm()
    
    return render(request, 'servicetype_form.html', {
        'form': form,
        'title': 'Create New Service Type'
    })

@token_required
def ServiceTypeUpdateView(request, servicetype_id):
    service_type = ServiceType.objects.get(id=servicetype_id)
    
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "servicetype_list"))
    else:
        form = ServiceTypeForm(instance=service_type)
    
    return render(request, 'servicetype_form.html', {
        'form': form,
        'title': 'Update Service Type',
        'service_type': service_type
    })

@token_required
def ServiceTypeDeleteView(request, servicetype_id):
    service_type = ServiceType.objects.get(id=servicetype_id)
    
    if request.method == 'POST':
        service_type.delete()
        #  Go back to where user came from
        return redirect(request.GET.get("next", "servicetype_list"))
    
    return render(request, 'servicetype_confirm_delete.html', {'service_type': service_type})