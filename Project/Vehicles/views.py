from django.shortcuts import render, redirect
from .models import Vehicle
from .forms import VehicleForm

def VehicleListView(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

def VehicleCreateView(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "vehicle_list"))
    else:
        form = VehicleForm()
    
    return render(request, 'vehicle_form.html', {
        'form': form,
        'title': 'Create New Vehicle'
    })

def VehicleUpdateView(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "vehicle_list"))
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicle_form.html', {
        'form': form,
        'title': 'Update Vehicle',
        'vehicle': vehicle
    })

def VehicleDeleteView(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    
    if request.method == 'POST':
        vehicle.delete()
        #  Go back to where user came from
        return redirect(request.GET.get("next", "vehicle_list"))
    
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})