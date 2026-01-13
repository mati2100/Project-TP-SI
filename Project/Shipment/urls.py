from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShipmentListView, name='shipment_list'),
    path('create/', views.ShipmentCreateView, name='shipment_create'),
    path('update/<int:shipment_id>/', views.ShipmentUpdateView, name='shipment_update'),
    path('delete/<int:shipment_id>/', views.ShipmentDeleteView, name='shipment_delete'),
]