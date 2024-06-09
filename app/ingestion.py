
import pandas as pd
from .models import Invoice, Total
from django.db.models import Sum
from collections import defaultdict

def ingest_excel(file_path):
    df = pd.read_excel(file_path)
    revenue_sources = set()
    
    for row in df.iterrows():
        revenue_source = row['Revenue source']
        
        _, created = Invoice.objects.get_or_create(
            invoice_number=row['invoice number'],
            customer=row['customer'],
            defaults={
                'date': row['date'],
                'value': row['value'],
                'haircut_percentage': row['haircut percent'],
                'daily_fee': row['Daily fee percent'],
                'currency': row['currency'],
                'revenue_source': revenue_source,
                'expected_duration': row['Expected payment duration']
            }
        )
           
        if created:
            revenue_sources.add(revenue_source)
    
    # Update totals only for the relevant revenue sources
    for revenue_source in revenue_sources:
        total_value = (Invoice.objects.filter(revenue_source=revenue_source).aggregate(total_value=Sum('value'))).get('total_value')
        # Assuming haircut percentage and daily fee are consistent for each revenue source
        first_invoice = Invoice.objects.filter(revenue_source=revenue_source).first()
        total_advance = total_value * (1 - (first_invoice.haircut_percentage / 100))
        total_expected_fee = total_advance * first_invoice.daily_fee * first_invoice.expected_duration

        Total.objects.update_or_create(
            revenue_source=revenue_source,
            defaults={
                'total_value': total_value,
                'total_advance': total_advance,
                'total_expected_fee': total_expected_fee
            }
        )
