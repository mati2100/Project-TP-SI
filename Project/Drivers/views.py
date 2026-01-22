from django.shortcuts import render, redirect
from .models import Driver
from .forms import DriverForm
from Profiles.decorators import token_required


@token_required
def DriverListView(request):
    drivers = Driver.objects.all()
    return render(request, 'driver_list.html', {'drivers': drivers})

@token_required
def DriverCreateView(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    
    return render(request, 'driver_form.html', {
        'form': form,
        'title': 'Create New Driver'
    })

@token_required
def DriverUpdateView(request, driver_id):
    driver = Driver.objects.get(id=driver_id)
    
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    
    return render(request, 'driver_form.html', {
        'form': form,
        'title': 'Update Driver',
        'driver': driver
    })

@token_required
def DriverDeleteView(request, driver_id):
    driver = Driver.objects.get(id=driver_id)
    
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    
    return render(request, 'driver_confirm_delete.html', {'driver': driver})