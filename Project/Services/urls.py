from django.urls import path
from . import views

urlpatterns = [
    # Destination URLs
    path('destinations/', views.DestinationListView, name='destination_list'),
    path('destinations/create/', views.DestinationCreateView, name='destination_create'),
    path('destinations/update/<int:destination_id>/', views.DestinationUpdateView, name='destination_update'),
    path('destinations/delete/<int:destination_id>/', views.DestinationDeleteView, name='destination_delete'),
    
    # Service Type URLs
    path('servicetypes/', views.ServiceTypeListView, name='servicetype_list'),
    path('servicetypes/create/', views.ServiceTypeCreateView, name='servicetype_create'),
    path('servicetypes/update/<int:servicetype_id>/', views.ServiceTypeUpdateView, name='servicetype_update'),
    path('servicetypes/delete/<int:servicetype_id>/', views.ServiceTypeDeleteView, name='servicetype_delete'),
]