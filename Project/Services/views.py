from django.shortcuts import render, redirect
from .models import Destination, ServiceType
from .forms import DestinationForm, ServiceTypeForm

# Destination Views
def DestinationListView(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

def DestinationCreateView(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm()
    
    return render(request, 'destination_form.html', {
        'form': form,
        'title': 'Create New Destination'
    })

def DestinationUpdateView(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm(instance=destination)
    
    return render(request, 'destination_form.html', {
        'form': form,
        'title': 'Update Destination',
        'destination': destination
    })

def DestinationDeleteView(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    
    if request.method == 'POST':
        destination.delete()
        return redirect('destination_list')
    
    return render(request, 'destination_confirm_delete.html', {'destination': destination})

# Service Type Views
def ServiceTypeListView(request):
    service_types = ServiceType.objects.all()
    return render(request, 'servicetype_list.html', {'service_types': service_types})

def ServiceTypeCreateView(request):
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicetype_list')
    else:
        form = ServiceTypeForm()
    
    return render(request, 'servicetype_form.html', {
        'form': form,
        'title': 'Create New Service Type'
    })

def ServiceTypeUpdateView(request, servicetype_id):
    service_type = ServiceType.objects.get(id=servicetype_id)
    
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            form.save()
            return redirect('servicetype_list')
    else:
        form = ServiceTypeForm(instance=service_type)
    
    return render(request, 'servicetype_form.html', {
        'form': form,
        'title': 'Update Service Type',
        'service_type': service_type
    })

def ServiceTypeDeleteView(request, servicetype_id):
    service_type = ServiceType.objects.get(id=servicetype_id)
    
    if request.method == 'POST':
        service_type.delete()
        return redirect('servicetype_list')
    
    return render(request, 'servicetype_confirm_delete.html', {'service_type': service_type})