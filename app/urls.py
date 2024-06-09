from django.urls import path
from . import views

urlpatterns = [
    path('upload-invoices/', views.upload_invoices, name='upload_invoices'),
    path('invoice-totals/', views.invoice_totals, name='invoice_totals'),
]
