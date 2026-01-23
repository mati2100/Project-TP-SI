from django.urls import path
from . import views

urlpatterns = [
    path('', views.PackageListView, name='package_list'),
    path('create/', views.PackageCreateView, name='package_create'),
    path('update/<int:package_id>/', views.PackageUpdateView, name='package_update'),
    path('delete/<int:package_id>/', views.PackageDeleteView, name='package_delete'),
]