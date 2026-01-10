from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncidentListView, name='incident_list'),
    path('create/', views.IncidentCreateView, name='incident_create'),
    path('update/<int:incident_id>/', views.IncidentUpdateView, name='incident_update'),
    path('delete/<int:incident_id>/', views.IncidentDeleteView, name='incident_delete'),
]