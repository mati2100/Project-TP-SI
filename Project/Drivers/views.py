from django.shortcuts import render, redirect
from .models import Driver
from .forms import DriverForm

def DriverListView(request):
    drivers = Driver.objects.all()
    return render(request, 'driver_list.html', {'drivers': drivers})

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

def DriverDeleteView(request, driver_id):
    driver = Driver.objects.get(id=driver_id)
    
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    
    return render(request, 'driver_confirm_delete.html', {'driver': driver})