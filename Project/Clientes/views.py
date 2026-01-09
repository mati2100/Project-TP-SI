from django.shortcuts import render, redirect
from .models import Client
from .forms import ClientForm

def ClientListView(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def ClientCreateView(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    
    return render(request, 'client_form.html', {
        'form': form,
        'title': 'Create New Client'
    })

def ClientUpdateView(request, client_id):
    client = Client.objects.get(id=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'client_form.html', {
        'form': form,
        'title': 'Update Client',
        'client': client
    })

def ClientDeleteView(request, client_id):
    client = Client.objects.get(id=client_id)
    
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    
    return render(request, 'client_confirm_delete.html', {'client': client})