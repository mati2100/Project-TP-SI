from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReclaimListView, name='reclaims_list'),
    path('create/', views.ReclaimCreateView, name='reclaims_create'),
    path('update/<int:reclaim_id>/', views.ReclaimUpdateView, name='reclaims_update'),
    path('delete/<int:reclaim_id>/', views.ReclaimDeleteView, name='reclaims_delete'),
]