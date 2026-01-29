from django.urls import path
from . import views

urlpatterns = [
    path('', views.InvoiceListView, name='invoice_list'),
    path('create/', views.InvoiceCreateView, name='invoice_create'),
    path('update/<int:invoice_id>/', views.InvoiceUpdateView, name='invoice_update'),
    path('delete/<int:invoice_id>/', views.InvoiceDeleteView, name='invoice_delete'),
    path('download/<int:invoice_id>/', views.invoice_download_pdf, name='invoice_download_pdf'),
    path('view/<int:invoice_id>/', views.invoice_view_pdf, name='invoice_view_pdf'),
]