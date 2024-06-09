
import os
import pandas as pd
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from app.models import Invoice, Total
from django.utils.timezone import now
from unittest.mock import patch

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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

    @patch('app.tasks.process_invoices.delay')
    def test_index_view_post(self, mock_process_invoices):
        with open(self.test_file_path, 'rb') as f:
            response = self.client.post(reverse('upload_invoice'), {'file': f})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        mock_process_invoices.assert_called_once()

    def test_get_invoice_totals_view(self):
        Total.objects.create(
            revenue_source='Source A',
            total_value=1000,
            total_advance=900,
            total_expected_fee=30
        )

        response = self.client.get(reverse('invoice_totals'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['revenue_source'], 'Source A')

    @patch('django.utils.timezone.now', return_value=now())
    def test_load_invoices_view(self, mock_now):
        Invoice.objects.create(
            date='2023-01-01',
            invoice_number=1,
            value=1000,
            haircut_percentage=10,
            daily_fee=1,
            currency='USD',
            revenue_source='Source A',
            customer='Customer A',
            expected_duration=30,
            created_at=mock_now()
        )

        response = self.client.get(reverse('load_invoices'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['invoices']), 1)
        self.assertEqual(response.json()['invoices'][0]['invoice_number'], 1)
