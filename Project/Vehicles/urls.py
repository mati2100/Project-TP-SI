from django.urls import path
from . import views

urlpatterns = [
    path('', views.VehicleListView, name='vehicle_list'),
    path('create/', views.VehicleCreateView, name='vehicle_create'),
    path('update/<int:vehicle_id>/', views.VehicleUpdateView, name='vehicle_update'),
    path('delete/<int:vehicle_id>/', views.VehicleDeleteView, name='vehicle_delete'),
]