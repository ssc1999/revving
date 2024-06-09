
from django.urls import path
from . import views

urlpatterns = [
    path('upload-invoice/', views.index, name='upload_invoice'),
    path('invoice-totals/', views.get_invoice_totals, name='invoice_totals'),
    path('invoices/', views.load_invoices, name='load_invoices'),
]
