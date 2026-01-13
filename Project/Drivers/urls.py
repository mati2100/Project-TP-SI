from django.urls import path
from . import views

urlpatterns = [
    path('', views.DriverListView, name='driver_list'),
    path('create/', views.DriverCreateView, name='driver_create'),
    path('update/<int:driver_id>/', views.DriverUpdateView, name='driver_update'),
    path('delete/<int:driver_id>/', views.DriverDeleteView, name='driver_delete'),
]