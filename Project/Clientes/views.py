from django.shortcuts import render, redirect
from .models import Client
from .forms import ClientForm

from django.db.models import Q

def ClientListView(request):
    clients = Client.objects.all()

    query = request.GET.get('q')
    search_by = request.GET.get('by')

    if query:
        if search_by == 'id':
            clients = clients.filter(id__icontains=query)
        elif search_by == 'email':
            clients = clients.filter(client_email__icontains=query)
        else:  # name (default)
            clients = clients.filter(
                Q(client_firstname__icontains=query) |
                Q(client_familyname__icontains=query)
            )

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