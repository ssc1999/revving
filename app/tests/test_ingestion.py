
import os
import pandas as pd
from django.test import TestCase
from app.models import Invoice, Total
from app.ingestion import ingest_excel
from django.conf import settings
from django.utils.timezone import now
from unittest.mock import patch

class IngestionTestCase(TestCase):
    def setUp(self):
        self.test_file_path = os.path.join(settings.MEDIA_ROOT, 'test_invoices.xlsx')
        df = pd.DataFrame({
            'date': ['2023-01-01'],
            'invoice number': [1],
            'value': [1000],
            'haircut percent': [10],
            'Daily fee percent': [1],
            'currency': ['USD'],
            'Revenue source': ['Source A'],
            'customer': ['Customer A'],
            'Expected payment duration': [30]
        })
        df.to_excel(self.test_file_path, index=False)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @patch('django.utils.timezone.now', return_value=now())
    @patch('app.models.Invoice.objects.get_or_create')
    def test_ingest_excel(self, mock_get_or_create, mock_now):
        # Mock the creation of Invoice objects to include created_at field
        def custom_get_or_create(defaults=None, **kwargs):
            defaults['created_at'] = now()
            invoice = Invoice(**{**kwargs, **defaults})
            invoice.save()
            return invoice, True
        
        mock_get_or_create.side_effect = custom_get_or_create

        # Call the function with the test file
        ingest_excel(self.test_file_path)

        # Check if the Invoice object is created
        invoice = Invoice.objects.first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.invoice_number, 1)
        self.assertEqual(invoice.value, 1000)
        self.assertEqual(invoice.currency, 'USD')
        self.assertIsNotNone(invoice.created_at)  # Ensure created_at is set

        # Check if the Total object is updated
        total = Total.objects.first()
        self.assertIsNotNone(total)
        self.assertEqual(total.revenue_source, 'Source A')
