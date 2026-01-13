from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeliveryTourListView, name='deliverytour_list'),
    path('create/', views.DeliveryTourCreateView, name='deliverytour_create'),
    path('update/<int:tour_id>/', views.DeliveryTourUpdateView, name='deliverytour_update'),
    path('delete/<int:tour_id>/', views.DeliveryTourDeleteView, name='deliverytour_delete'),
]